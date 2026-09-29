#!/usr/bin/env python3
"""
recommend.py - Accept a project brief and recommend optimal font pairings and typography architecture.

Accepts either CLI parameters or a project brief file (JSON or free-text).
Translates project goals, brand vibes, platform constraints, and scripts into mathematically
scored typography pairings with deep rationales and code implementation snippets.
"""

import os
import sys
import json
import argparse
import re
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

                         
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typography_engine import TypographyEngine, format_cli_project_plan

def parse_text_brief(text: str) -> Dict[str, Any]:
    """Parse unstructured text brief for use-case, style, and platform keywords."""
    low = text.lower()
    brief = {
        "use_case": "saas",
        "style": "",
        "platform": "web",
        "scripts": ["Latin"],
        "languages": ["en"]
    }

                      
    use_case_keywords = {
        "fintech": "fintech",
        "neobank": "fintech",
        "bank": "finance",
        "finance": "finance",
        "saas": "saas",
        "software": "saas",
        "landing": "landing-page",
        "portfolio": "portfolio",
        "dashboard": "dashboard",
        "analytics": "dashboard",
        "ecommerce": "ecommerce",
        "shop": "ecommerce",
        "store": "ecommerce",
        "fashion": "fashion",
        "luxury": "luxury",
        "restaurant": "restaurant",
        "food": "restaurant",
        "crypto": "crypto",
        "web3": "crypto",
        "education": "education",
        "gaming": "gaming",
        "game": "gaming",
        "news": "news",
        "blog": "blog",
        "editorial": "blog",
        "agency": "agency",
        "powerpoint": "powerpoint",
        "deck": "powerpoint",
        "slide": "powerpoint",
        "presentation": "presentation",
        "resume": "resume",
        "cv": "resume",
        "poster": "poster",
        "logo": "logo",
        "branding": "branding"
    }
    for kw, uc in use_case_keywords.items():
        if kw in low:
            brief["use_case"] = uc
            break

                     
    if "flutter" in low: brief["platform"] = "flutter"
    elif "react native" in low or "reactnative" in low: brief["platform"] = "react-native"
    elif "ios" in low or "iphone" in low: brief["platform"] = "ios"
    elif "android" in low: brief["platform"] = "android"
    elif "powerpoint" in low or "ppt" in low or "keynote" in low: brief["platform"] = "powerpoint"
    elif "word" in low or "doc" in low: brief["platform"] = "word"
    elif "pdf" in low: brief["platform"] = "pdf"
    elif "mobile" in low or "app" in low: brief["platform"] = "mobile"
    else: brief["platform"] = "web"

                        
    style_hits = []
    vibe_words = [
        "expensive", "premium", "luxury", "clean", "modern", "editorial",
        "futuristic", "playful", "professional", "not ai-looking", "brutalist",
        "minimal", "classic", "techno", "retro", "vintage", "humanist"
    ]
    for vw in vibe_words:
        if vw in low:
            style_hits.append(vw)
    if style_hits:
        brief["style"] = ", ".join(style_hits)

                    
    if "cyrillic" in low or "russian" in low or "ukrainian" in low:
        brief["scripts"].append("Cyrillic")
    if "greek" in low:
        brief["scripts"].append("Greek")
    if "bangla" in low or "bengali" in low:
        brief["scripts"].append("Bangla")
    if "arabic" in low:
        brief["scripts"].append("Arabic")
    if "devanagari" in low or "hindi" in low:
        brief["scripts"].append("Devanagari")
    if "korean" in low or "hangul" in low:
        brief["scripts"].append("Hangul")

    return brief

def run_recommendation(
    engine: TypographyEngine,
    use_case: str,
    style: str = "",
    platform: str = "",
    scripts: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    anchor_font: Optional[str] = None,
    existing_fonts: Optional[List[str]] = None,
    limit: int = 3
) -> Dict[str, Any]:
    """Execute recommendation through the decision engine."""
    return engine.plan_project_typography(
        use_case_id=use_case,
        style_vibe=style,
        platform=platform,
        target_scripts=scripts or ["Latin"],
        target_languages=languages or ["en"],
        anchor_font=anchor_font,
        existing_fonts=existing_fonts,
        limit=limit
    )

def main():
    parser = argparse.ArgumentParser(
        description="Recommend optimal font pairings and typography architecture based on a project brief."
    )
    parser.add_argument("--brief", "-b", default=None, help="Path to brief file (.json or .txt)")
    parser.add_argument("--use-case", "-u", default=None, help="Project use case (e.g. saas, fintech, dashboard, powerpoint, etc.)")
    parser.add_argument("--style", "-s", default="", help="Design vibe or style query (e.g. 'expensive, not AI-looking', 'clean modern')")
    parser.add_argument("--platform", "-p", default="", help="Target platform (web, flutter, react-native, ios, android, powerpoint)")
    parser.add_argument("--scripts", default="Latin", help="Comma-separated target scripts (e.g. 'Latin, Cyrillic' or 'Bangla')")
    parser.add_argument("--languages", default="en", help="Comma-separated target ISO language codes (e.g. 'en, de')")
    parser.add_argument("--anchor", "-a", default=None, help="Explicit user font selection to anchor around (e.g. 'Chillax' or 'Poppins')")
    parser.add_argument("--existing-fonts", default=None, help="Existing fonts in project to preserve/integrate (e.g. 'Inter, Roboto')")
    parser.add_argument("--limit", "-n", type=int, default=3, help="Number of pairings to return (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    engine = TypographyEngine()

    use_case = args.use_case
    style = args.style
    platform = args.platform
    anchor_font = args.anchor
    existing_fonts = [ef.strip() for ef in args.existing_fonts.split(",") if ef.strip()] if args.existing_fonts else None
    scripts = [s.strip() for s in args.scripts.split(",") if s.strip()]
    languages = [l.strip() for l in args.languages.split(",") if l.strip()]

                                                    
    if args.brief:
        if not os.path.exists(args.brief):
            print(f"Error: Brief file '{args.brief}' not found.", file=sys.stderr)
            sys.exit(1)

        with open(args.brief, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if args.brief.endswith(".json") or content.startswith("{"):
            try:
                b_data = json.loads(content)
                use_case = b_data.get("use_case", use_case or "saas")
                style = b_data.get("style", style)
                platform = b_data.get("platform", platform or "web")
                if "scripts" in b_data:
                    scripts = b_data["scripts"] if isinstance(b_data["scripts"], list) else [b_data["scripts"]]
                if "languages" in b_data:
                    languages = b_data["languages"] if isinstance(b_data["languages"], list) else [b_data["languages"]]
            except Exception as e:
                print(f"Error parsing JSON brief: {e}", file=sys.stderr)
                sys.exit(1)
        else:
                               
            parsed = parse_text_brief(content)
            use_case = use_case or parsed["use_case"]
            style = style or parsed["style"]
            platform = platform or parsed["platform"]
            if parsed.get("scripts"):
                scripts = parsed["scripts"]

    if not use_case:
        use_case = "saas"

    try:
        plan = run_recommendation(
            engine=engine,
            use_case=use_case,
            style=style,
            platform=platform,
            scripts=scripts,
            languages=languages,
            anchor_font=anchor_font,
            existing_fonts=existing_fonts,
            limit=args.limit
        )
    except Exception as e:
        print(f"Recommendation error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(plan, indent=2))
    else:
        print(format_cli_project_plan(plan))

if __name__ == "__main__":
    main()
