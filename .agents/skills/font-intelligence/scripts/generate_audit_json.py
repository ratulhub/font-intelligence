#!/usr/bin/env python3
"""
generate_audit_json.py - Generate machine-readable docs/repository-audit.json.
Audits all source packages in 'All fonts/', file formats, licenses, readmes, previews, and integrity hashes.
"""

import os
import sys
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(ROOT_DIR, "All fonts")
OUT_JSON = os.path.join(ROOT_DIR, "docs", "repository-audit.json")


def generate_audit():
    audit = {
        "generated_at": "2026-09-29T12:00:00+00:00",
        "total_packages": 0,
        "total_font_files": 0,
        "formats": {},
        "packages": {},
        "summary": {
            "variable_fonts_count": 0,
            "italic_files_count": 0,
            "preview_assets_count": 0,
            "license_files_count": 0,
            "readme_files_count": 0,
            "misc_directories_count": 0,
            "suspicious_files": [],
            "duplicate_binaries": [],
            "missing_licenses": [],
            "ambiguous_licensing": []
        }
    }

    hashes = {}
    packages = sorted([d for d in os.listdir(FONTS_DIR) if os.path.isdir(os.path.join(FONTS_DIR, d))])
    audit["total_packages"] = len(packages)

    for pkg in packages:
        pkg_path = os.path.join(FONTS_DIR, pkg)
        font_files = []
        licenses = []
        readmes = []
        previews = []
        misc_files = []

        for r, dirs, files in os.walk(pkg_path):
            for f in files:
                full = os.path.join(r, f)
                rel = os.path.relpath(full, ROOT_DIR).replace("\\", "/")
                ext = os.path.splitext(f)[1].lower()
                fname_lower = f.lower()

                if ext in [".ttf", ".otf", ".woff", ".woff2", ".ttc", ".dfont"]:
                    audit["total_font_files"] += 1
                    fmt = ext.replace(".", "")
                    audit["formats"][fmt] = audit["formats"].get(fmt, 0) + 1

                    # compute sha256
                    with open(full, "rb") as fb:
                        h = hashlib.sha256(fb.read()).hexdigest()

                    if h in hashes:
                        audit["summary"]["duplicate_binaries"].append({
                            "original_file": hashes[h],
                            "duplicate_file": rel,
                            "sha256": h
                        })
                    else:
                        hashes[h] = rel

                    is_italic = any(k in fname_lower for k in ["italic", "ital", " it."])
                    if is_italic:
                        audit["summary"]["italic_files_count"] += 1

                    is_var = any(k in fname_lower for k in ["variable", "var."])
                    if is_var:
                        audit["summary"]["variable_fonts_count"] += 1

                    font_files.append({
                        "file": rel,
                        "format": fmt,
                        "size_bytes": os.path.getsize(full),
                        "sha256": h,
                        "italic": is_italic,
                        "variable_candidate": is_var
                    })
                elif any(k in fname_lower for k in ["license", "ofl", "licence", "copying", "eula"]):
                    licenses.append(rel)
                    audit["summary"]["license_files_count"] += 1
                elif any(k in fname_lower for k in ["readme", "about", "info", "fontlog", "read me"]):
                    readmes.append(rel)
                    audit["summary"]["readme_files_count"] += 1
                elif ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]:
                    previews.append(rel)
                    audit["summary"]["preview_assets_count"] += 1
                else:
                    misc_files.append(rel)
                    if ext in [".exe", ".bat", ".sh", ".vbs", ".scr"]:
                        audit["summary"]["suspicious_files"].append(rel)

        has_misc_dir = os.path.exists(os.path.join(pkg_path, "misc"))
        if has_misc_dir:
            audit["summary"]["misc_directories_count"] += 1

        if not licenses:
            audit["summary"]["missing_licenses"].append(pkg)

        audit["packages"][pkg] = {
            "package_name": pkg,
            "font_file_count": len(font_files),
            "fonts": font_files,
            "licenses": licenses,
            "readmes": readmes,
            "previews": previews,
            "misc_files": misc_files,
            "has_misc_dir": has_misc_dir
        }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as out_f:
        json.dump(audit, out_f, indent=2)

    print(f"Generated {OUT_JSON}: {audit['total_packages']} packages, {audit['total_font_files']} font files.")


if __name__ == "__main__":
    generate_audit()
