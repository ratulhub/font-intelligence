#!/usr/bin/env python3
"""
generate_preview.py - Compiles preview/fonts-data.js from catalog/fonts.json.
Allows the preview studio to run completely offline without CORS restrictions.
"""

import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
PREVIEW_DATA_JS = os.path.join(ROOT_DIR, "preview", "fonts-data.js")

def main():
    if not os.path.exists(CATALOG_PATH):
        print(f"Error: Catalog not found at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

                               
    js_content = f"window.CATALOG_DATA = {json.dumps(catalog)};\n"

    os.makedirs(os.path.dirname(PREVIEW_DATA_JS), exist_ok=True)
    with open(PREVIEW_DATA_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {PREVIEW_DATA_JS} ({catalog['total_families']} font families, {len(js_content):,} bytes).")

if __name__ == "__main__":
    main()
