#!/usr/bin/env python3
"""
score_pair.py - Score two fonts against a specific project context across 10 dimensions.

Evaluates visual contrast, serif/sans relationship, personality resonance, readability,
proportional width, weight ladder, role compatibility, project style, script parity,
and platform suitability. Checks 10 typographic anti-patterns with point deductions.
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typography_engine import TypographyEngine, format_cli_evaluation


def main():
    parser = argparse.ArgumentParser(
        description="Score any two fonts against a specific project context across 10 dimensions."
    )
    parser.add_argument("--primary", "-p", required=True, help="Primary font ID or family name (e.g. chillax, general-sans, ithaca)")
    parser.add_argument("--secondary", "-s", required=True, help="Secondary font ID or family name (e.g. general-sans, ubuntu, credit-valley)")
    parser.add_argument("--primary-role", default="heading", help="Role for primary font (default: heading)")
    parser.add_argument("--secondary-role", default="body", help="Role for secondary font (default: body)")
    parser.add_argument("--primary-weight", type=int, default=None, help="Explicit weight for primary font (e.g. 700, 800)")
    parser.add_argument("--secondary-weight", type=int, default=None, help="Explicit weight for secondary font (e.g. 400)")
    parser.add_argument("--use-case", default=None, help="Optional project use case (saas, fintech, dashboard, blog, etc.)")
    parser.add_argument("--style", default="modern", help="Brand style / vibe (e.g. modern, luxury, brutalist, minimal, playful)")
    parser.add_argument("--platform", default="web", help="Target platform (web, flutter, react-native, powerpoint, print)")
    parser.add_argument("--scripts", default="Latin", help="Target scripts (comma-separated, default: Latin)")
    parser.add_argument("--languages", default="en", help="Target language codes (comma-separated, default: en)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON evaluation data")

    args = parser.parse_args()
    engine = TypographyEngine()

    p_font = engine.get_font(args.primary)
    s_font = engine.get_font(args.secondary)

    if not p_font:
        print(f"Error: Primary font '{args.primary}' not found in catalog.", file=sys.stderr)
        print("Tip: Run search_fonts.py to find available fonts.", file=sys.stderr)
        sys.exit(1)

    if not s_font:
        print(f"Error: Secondary font '{args.secondary}' not found in catalog.", file=sys.stderr)
        print("Tip: Run search_fonts.py to find available fonts.", file=sys.stderr)
        sys.exit(1)

    # If use-case provided, pull style if not overridden
    effective_style = args.style
    if args.use_case:
        uc = engine.get_use_case(args.use_case)
        if uc and args.style == "modern":
            effective_style = uc.get("key_requirements", {}).get("ideal_styles", ["modern"])[0]

    ctx = {
        "project_style": effective_style,
        "platform": args.platform,
        "primary_role": args.primary_role,
        "secondary_role": args.secondary_role,
        "languages": [l.strip() for l in args.languages.split(",") if l.strip()]
    }
    if args.primary_weight:
        ctx["primary_weight"] = args.primary_weight
    if args.secondary_weight:
        ctx["secondary_weight"] = args.secondary_weight

    try:
        eval_res = engine.evaluate_pairing(
            primary_font=p_font,
            secondary_font=s_font,
            context=ctx
        )
    except Exception as e:
        print(f"Scoring error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(eval_res, indent=2))
    else:
        print(format_cli_evaluation(eval_res))


if __name__ == "__main__":
    main()
