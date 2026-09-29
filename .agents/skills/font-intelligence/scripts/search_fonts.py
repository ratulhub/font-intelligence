#!/usr/bin/env python3
"""
search_fonts.py - Search font catalog by use, style, mood, role, language/script, category, and platform.

Allows rich multi-criteria filtering across the verified font intelligence catalog,
including minimum readability thresholds, mood/vibe translation, and platform compatibility.
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not os.path.exists(os.path.join(ROOT_DIR, "catalog")):
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
USE_CASES_PATH = os.path.join(ROOT_DIR, "catalog", "use-cases.json")


def load_catalog_and_use_cases(cat_path: str, uc_path: str):
    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    use_cases = {}
    style_interp = {}
    if os.path.exists(uc_path):
        with open(uc_path, "r", encoding="utf-8") as f:
            uc_data = json.load(f)
            use_cases = uc_data.get("use_cases", {})
            style_interp = uc_data.get("style_interpretations", {})
    return catalog.get("fonts", []), use_cases, style_interp


def search_fonts(
    fonts: List[Dict[str, Any]],
    use_cases: Dict[str, Any],
    style_interp: Dict[str, Any],
    query: Optional[str] = None,
    use_case: Optional[str] = None,
    style: Optional[str] = None,
    mood: Optional[str] = None,
    role: Optional[str] = None,
    script: Optional[str] = None,
    language: Optional[str] = None,
    category: Optional[str] = None,
    platform: Optional[str] = None,
    min_readability: int = 0,
    variable_only: bool = False
) -> List[Dict[str, Any]]:
    """Filter catalog fonts by multiple criteria."""
    results = []

    # Map use-case to requirements
    uc_styles = []
    uc_roles = []
    if use_case:
        uc_clean = use_case.lower().strip()
        uc_info = use_cases.get(uc_clean)
        if uc_info:
            uc_styles = [s.lower() for s in uc_info.get("key_requirements", {}).get("ideal_styles", [])]
            uc_roles = [r.lower() for r in uc_info.get("key_requirements", {}).get("typography_roles", [])]

    # Map mood to styles
    mood_styles = []
    mood_cats = []
    if mood:
        m_low = mood.lower().strip()
        for k, v in style_interp.items():
            if k in m_low or m_low in k:
                prof = v.get("typographic_profile", {})
                mood_styles.extend([s.lower() for s in prof.get("preferred_styles", [])])
                mood_cats.extend([c.lower() for c in prof.get("primary_categories", [])])
        if not mood_styles:
            mood_styles = [m_low]

    for f in fonts:
        cur = f.get("curated", {})
        tech = f.get("technical", {})
        f_name = f.get("name", "")
        f_id = f.get("id", "")
        f_cat = cur.get("category", "").lower()
        f_styles = [s.lower() for s in cur.get("styles", [])]
        f_roles = [r.lower() for r in cur.get("roles", [])]
        f_scripts = [s.lower() for s in tech.get("scripts", [])] + [b.lower() for b in tech.get("unicode_blocks", [])]
        f_langs = [l.lower() for l in tech.get("languages", [])]
        f_read = cur.get("readability", {})

        # Free-text Query
        if query:
            q_clean = query.lower()
            text_corpus = f"{f_id} {f_name} {f_cat} {' '.join(f_styles)} {' '.join(f_roles)} {cur.get('notes', '')}".lower()
            if q_clean not in text_corpus:
                continue

        # Category
        if category and category.lower() != f_cat:
            continue

        # Mood categories filter
        if mood_cats and f_cat not in mood_cats:
            continue

        # Style
        if style:
            req_style = style.lower().strip()
            if req_style not in f_styles:
                continue

        # Mood styles
        if mood_styles:
            if not any(ms in f_styles for ms in mood_styles):
                continue

        # Use case styles/roles
        if uc_styles and not any(us in f_styles for us in uc_styles):
            continue

        # Role
        if role:
            req_role = role.lower().strip()
            if req_role not in f_roles:
                continue

        # Script
        if script:
            req_script = script.lower().strip()
            if not any(req_script in s for s in f_scripts):
                continue

        # Language
        if language:
            req_lang = language.lower().strip()
            if req_lang not in f_langs:
                continue

        # Variable only
        if variable_only and not tech.get("variable", False):
            continue

        # Platform check
        if platform:
            plat_clean = platform.lower().strip()
            if plat_clean in ["powerpoint", "word", "office"]:
                # Must have ttf format and permissive embedding
                has_ttf = any(file_info.get("format") == "ttf" for file_info in f.get("files", []))
                fs_perm = tech.get("embedding_permission", "")
                if not has_ttf or "Restricted" in fs_perm:
                    continue
            elif plat_clean in ["web"]:
                has_web = any(file_info.get("format") in ["woff2", "woff", "ttf"] for file_info in f.get("files", []))
                if not has_web:
                    continue

        # Min readability
        if min_readability > 0:
            target_prop = role.lower() if role in ["body", "ui", "numbers", "long_form", "small_text"] else "body"
            score = f_read.get(target_prop, 0)
            if score < min_readability:
                continue

        results.append(f)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Search font catalog by use, style, mood, role, language/script, category, and platform."
    )
    parser.add_argument("--query", "-q", default=None, help="Free-text search term across name, notes, styles")
    parser.add_argument("--use", "--use-case", dest="use_case", default=None, help="Use case (e.g. saas, fintech, dashboard, luxury, etc.)")
    parser.add_argument("--style", default=None, help="Style category (e.g. modern, brutalist, minimal, luxury, etc.)")
    parser.add_argument("--mood", default=None, help="Colloquial vibe (e.g. 'expensive', 'clean', 'editorial', 'not AI-looking')")
    parser.add_argument("--role", default=None, help="Typography role (heading, body, ui, number, code, display, hero)")
    parser.add_argument("--script", default=None, help="Script support (Latin, Cyrillic, Greek, Devanagari, Bangla, Arabic)")
    parser.add_argument("--language", default=None, help="Language code (en, de, fr, es, pl, cs)")
    parser.add_argument("--category", default=None, choices=["sans-serif", "serif", "display", "monospace", "handwriting"], help="Font category")
    parser.add_argument("--platform", default=None, help="Platform target (web, mobile, flutter, react-native, powerpoint)")
    parser.add_argument("--min-readability", type=int, default=0, help="Minimum readability score (1-10) for assigned role")
    parser.add_argument("--variable-only", action="store_true", help="Only show variable fonts")
    parser.add_argument("--format", choices=["table", "detailed", "json", "ids"], default="table", help="Output format (default: table)")
    parser.add_argument("--limit", type=int, default=50, help="Max results to display")
    parser.add_argument("--catalog", default=CATALOG_PATH, help="Path to fonts.json")

    args = parser.parse_args()

    if not os.path.exists(args.catalog):
        print(f"Error: Catalog file '{args.catalog}' not found.", file=sys.stderr)
        sys.exit(1)

    fonts, use_cases, style_interp = load_catalog_and_use_cases(args.catalog, USE_CASES_PATH)

    results = search_fonts(
        fonts=fonts,
        use_cases=use_cases,
        style_interp=style_interp,
        query=args.query,
        use_case=args.use_case,
        style=args.style,
        mood=args.mood,
        role=args.role,
        script=args.script,
        language=args.language,
        category=args.category,
        platform=args.platform,
        min_readability=args.min_readability,
        variable_only=args.variable_only
    )

    total_matches = len(results)
    results = results[:args.limit]

    if args.format == "json":
        print(json.dumps(results, indent=2))
        return

    if args.format == "ids":
        for r in results:
            print(r["id"])
        return

    print("=" * 80)
    print(f"FONT SEARCH RESULTS ({len(results)} of {total_matches} matched)")
    print("=" * 80)

    if not results:
        print("No fonts matched your search criteria.")
        print("Tip: Broaden filters or check available scripts with scan_fonts.py.")
        print("=" * 80)
        return

    if args.format == "detailed":
        for idx, f in enumerate(results, 1):
            cur = f.get("curated", {})
            tech = f.get("technical", {})
            read = cur.get("readability", {})
            var_str = f" [VAR: {len(tech.get('axes', []))} axes]" if tech.get("variable") else ""
            print(f"[{idx}] {f['name']} ({cur.get('category')}) — ID: {f['id']}{var_str}")
            print(f"    Subtype:      {cur.get('subtype')}")
            print(f"    Styles:       {', '.join(cur.get('styles', []))}")
            print(f"    Roles:        {', '.join(cur.get('roles', []))}")
            print(f"    Readability:  Body: {read.get('body')}/10 | UI: {read.get('ui')}/10 | Long-form: {read.get('long_form')}/10")
            print(f"    Weights:      {tech.get('weights')}")
            print(f"    Scripts:      {', '.join(tech.get('scripts', []))}")
            print(f"    Embedding:    {tech.get('embedding_permission')}")
            print(f"    Notes:        {cur.get('notes')}\n")
    else:
        # Table view
        header = f"{'ID':<18} {'FAMILY NAME':<20} {'CATEGORY':<12} {'WEIGHTS':<15} {'BODY':<5} {'UI':<4} {'SCRIPTS'}"
        print(header)
        print("-" * 80)
        for f in results:
            cur = f.get("curated", {})
            tech = f.get("technical", {})
            read = cur.get("readability", {})
            w_str = f"{len(tech.get('weights', []))} weights"
            if tech.get("variable"):
                w_str += " (Var)"
            scripts_str = ", ".join(tech.get("scripts", [])[:3])
            b_score = str(read.get("body", "-"))
            ui_score = str(read.get("ui", "-"))
            print(f"{f['id'][:17]:<18} {f['name'][:19]:<20} {cur.get('category', '')[:11]:<12} {w_str[:14]:<15} {b_score:<5} {ui_score:<4} {scripts_str}")

    print("=" * 80)


if __name__ == "__main__":
    main()
