#!/usr/bin/env python3
"""
clean_project.py - Zero-bloat post-project typography cleaner.

Ensures only used font files stay in the user's project folder.
Deletes unneeded fonts, extra weights, and local skill folders so the project remains lightweight.
"""

import os
import sys
import shutil
import argparse
import re
from typing import Dict, List, Set, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_EXTENSIONS = {".woff2", ".woff", ".ttf", ".otf", ".eot"}

def is_canonical_repo(path: str) -> bool:
    abs_p = os.path.abspath(path)
    if abs_p == ROOT_DIR:
        return True
    if os.path.exists(os.path.join(abs_p, "catalog", "fonts.json")) and os.path.exists(os.path.join(abs_p, "All fonts")):
        return True
    return False

def find_font_references_in_code(project_dir: str) -> Set[str]:
    referenced = set()
    code_exts = {".css", ".scss", ".sass", ".less", ".html", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".dart", ".json", ".yaml", ".yml"}
    
    url_pattern = re.compile(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', re.IGNORECASE)
    asset_pattern = re.compile(r'[\'"]([^\'"]+?\.(?:woff2|woff|ttf|otf|eot))[\'"]', re.IGNORECASE)

    for root, dirs, files in os.walk(project_dir):
        if any(ignored in root for ignored in [".git", "node_modules", ".venv", "venv", "__pycache__"]):
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in code_exts:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                    for m in url_pattern.findall(content):
                        cleaned = os.path.basename(m.split("?")[0].split("#")[0].strip())
                        if any(cleaned.lower().endswith(fext) for fext in FONT_EXTENSIONS):
                            referenced.add(cleaned.lower())
                    for m in asset_pattern.findall(content):
                        cleaned = os.path.basename(m.split("?")[0].split("#")[0].strip())
                        referenced.add(cleaned.lower())
                except Exception:
                    pass
    return referenced

def clean_project(
    project_dir: str,
    font_dir: Optional[str] = None,
    keep_fonts: Optional[List[str]] = None,
    clean_skill: bool = True,
    dry_run: bool = False
) -> Dict[str, Any]:
    project_abs = os.path.abspath(project_dir)
    report = {
        "project_dir": project_abs,
        "kept_fonts": [],
        "deleted_fonts": [],
        "deleted_folders": [],
        "bytes_freed": 0,
        "dry_run": dry_run,
        "status": "SUCCESS"
    }

    if is_canonical_repo(project_abs):
        print(f"[PROTECTED] Target '{project_abs}' is the Font Intelligence repository root. Clean aborted.", file=sys.stderr)
        report["status"] = "PROTECTED_ROOT_ABORTED"
        return report

    if not os.path.exists(project_abs):
        print(f"Error: Project directory '{project_abs}' does not exist.", file=sys.stderr)
        report["status"] = "NOT_FOUND"
        return report

    keep_filenames = set()
    if keep_fonts:
        for k in keep_fonts:
            cleaned = k.strip().lower()
            if cleaned:
                keep_filenames.add(cleaned)
                if not any(cleaned.endswith(fext) for fext in FONT_EXTENSIONS):
                    keep_filenames.add(f"{cleaned}.woff2")
                    keep_filenames.add(f"{cleaned}.ttf")
                    keep_filenames.add(f"{cleaned}.otf")

    detected_refs = find_font_references_in_code(project_abs)
    keep_filenames.update(detected_refs)

    candidate_font_dirs = []
    if font_dir:
        candidate_font_dirs.append(os.path.abspath(os.path.join(project_abs, font_dir)))
    else:
        for root, dirs, files in os.walk(project_abs):
            if any(ignored in root for ignored in [".git", "node_modules", ".venv", "venv", "__pycache__"]):
                continue
            for f in files:
                if os.path.splitext(f)[1].lower() in FONT_EXTENSIONS:
                    if root not in candidate_font_dirs:
                        candidate_font_dirs.append(root)

    for fdir in candidate_font_dirs:
        if not os.path.exists(fdir):
            continue
        try:
            for item in os.listdir(fdir):
                item_path = os.path.join(fdir, item)
                if not os.path.isfile(item_path):
                    continue
                ext = os.path.splitext(item)[1].lower()
                if ext in FONT_EXTENSIONS:
                    item_lower = item.lower()
                    should_keep = False
                    if not keep_filenames:
                        should_keep = True
                    else:
                        for k in keep_filenames:
                            if k == item_lower or k in item_lower:
                                should_keep = True
                                break
                    if should_keep:
                        report["kept_fonts"].append(item_path)
                    else:
                        sz = os.path.getsize(item_path)
                        report["deleted_fonts"].append(item_path)
                        report["bytes_freed"] += sz
                        if not dry_run:
                            os.remove(item_path)
        except Exception as e:
            print(f"Warning reading font dir '{fdir}': {e}", file=sys.stderr)

    if clean_skill:
        skill_paths = [
            os.path.join(project_abs, ".agents", "skills", "font-intelligence"),
            os.path.join(project_abs, ".agents", "skills"),
            os.path.join(project_abs, "font-intelligence")
        ]
        for sp in skill_paths:
            if os.path.exists(sp) and os.path.isdir(sp):
                if is_canonical_repo(sp):
                    continue
                dir_sz = sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(sp) for f in fs)
                report["deleted_folders"].append(sp)
                report["bytes_freed"] += dir_sz
                if not dry_run:
                    shutil.rmtree(sp, ignore_errors=True)

    return report

def main():
    parser = argparse.ArgumentParser(
        description="Clean unneeded font files and skill folders from a user project after creation."
    )
    parser.add_argument("--project-dir", "-p", default=".", help="Target project root directory (default: current directory)")
    parser.add_argument("--font-dir", "-f", default=None, help="Specific fonts directory inside project (e.g. 'public/fonts' or 'src/assets/fonts')")
    parser.add_argument("--keep-fonts", "-k", default=None, help="Comma-separated font names/IDs to keep (e.g. 'chillax,general-sans')")
    parser.add_argument("--no-clean-skill", dest="clean_skill", action="store_false", default=True, help="Do not delete local skill folder from project")
    parser.add_argument("--dry-run", action="store_true", help="Preview deletions without deleting anything")

    args = parser.parse_args()

    keep_list = [k.strip() for k in args.keep_fonts.split(",") if k.strip()] if args.keep_fonts else None

    res = clean_project(
        project_dir=args.project_dir,
        font_dir=args.font_dir,
        keep_fonts=keep_list,
        clean_skill=args.clean_skill,
        dry_run=args.dry_run
    )

    print("=" * 80)
    print("FONT INTELLIGENCE: ZERO-BLOAT PROJECT CLEANUP REPORT")
    print("=" * 80)
    print(f"• Target Project:    {res['project_dir']}")
    print(f"• Dry Run:           {'YES (Preview only)' if res['dry_run'] else 'NO (Files removed)'}")
    print(f"• Preserved Fonts:   {len(res['kept_fonts'])}")
    for kf in res['kept_fonts']:
        print(f"  ✓ [KEPT] {os.path.basename(kf)}")
    print(f"• Deleted Fonts:     {len(res['deleted_fonts'])}")
    for df in res['deleted_fonts']:
        print(f"  ✗ [DELETED] {os.path.basename(df)}")
    print(f"• Deleted Folders:   {len(res['deleted_folders'])}")
    for dfolder in res['deleted_folders']:
        print(f"  ✗ [REMOVED DIR] {dfolder}")
    print(f"• Space Saved:       {res['bytes_freed'] / 1024:.1f} KB")
    print("=" * 80)

if __name__ == "__main__":
    main()
