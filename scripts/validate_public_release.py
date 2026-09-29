#!/usr/bin/env python3
"""
validate_public_release.py - Public Asset Separation & Redistribution Gatekeeper

Scans assets/fonts/ to ensure ONLY legally redistributable fonts ('public-asset')
are present. Strictly blocks any 'catalog-only', 'restricted', or 'unknown' binaries.
"""

import sys
import os
import json
import argparse
from typing import Dict, List, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
ASSETS_FONTS_DIR = os.path.join(ROOT_DIR, "assets", "fonts")

def validate_public_release(catalog_path: str = CATALOG_PATH, assets_dir: str = ASSETS_FONTS_DIR) -> int:
    print("=" * 80)
    print("FONT INTELLIGENCE: PUBLIC ASSET RELEASE GATE")
    print("=" * 80)

    if not os.path.exists(catalog_path):
        print(f"[FAIL] Catalog not found at {catalog_path}")
        return 1

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    fonts_by_id: Dict[str, Dict[str, Any]] = {f["id"]: f for f in catalog.get("fonts", [])}

    if not os.path.exists(assets_dir):
        print(f"[WARN] Assets directory does not exist: {assets_dir}")
        return 0

    asset_folders = sorted([d for d in os.listdir(assets_dir) if os.path.isdir(os.path.join(assets_dir, d))])
    print(f"• Total Families in assets/fonts/: {len(asset_folders)}")

    violations = []
    allowed_assets = []

    for fid in asset_folders:
        folder_path = os.path.join(assets_dir, fid)
        font_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.ttf', '.otf', '.woff', '.woff2', '.ttc', '.dfont'))]

        if fid not in fonts_by_id:
            violations.append({
                "id": fid,
                "reason": "Uncataloged family in assets/fonts/ (not found in catalog/fonts.json)",
                "status": "UNREGISTERED",
                "files": font_files
            })
            continue

        entry = fonts_by_id[fid]
        dist_status = entry.get("distribution_status", "unknown")
        lic = entry.get("license", {})
        redist_allowed = lic.get("redistribution_allowed", False)

        if dist_status != "public-asset":
            violations.append({
                "id": fid,
                "reason": f"Distribution status is '{dist_status}', expected 'public-asset'",
                "status": dist_status,
                "license": lic.get("type", "Unknown"),
                "files": font_files
            })
        elif not redist_allowed:
            violations.append({
                "id": fid,
                "reason": "redistribution_allowed is False in catalog metadata",
                "status": dist_status,
                "license": lic.get("type", "Unknown"),
                "files": font_files
            })
        else:
            allowed_assets.append({
                "id": fid,
                "name": entry.get("name", fid),
                "license": lic.get("type", "Permissive"),
                "file_count": len(font_files)
            })

    print("-" * 80)
    if violations:
        print(f"[FAIL] DETECTED {len(violations)} RESTRICTED OR UNVERIFIED FONTS IN assets/fonts/:\n")
        print(f"{'FAMILY ID':<25} {'STATUS':<15} {'VIOLATION REASON'}")
        print("-" * 80)
        for v in violations:
            print(f"{v['id']:<25} {v['status']:<15} {v['reason']}")
        print("=" * 80)
        print("PUBLIC ASSET VALIDATION: FAILED")
        print("Run scripts/build_release_manifest.py to purge non-public assets.")
        print("=" * 80)
        return 1
    else:
        print(f"[PASS] All {len(allowed_assets)} families in assets/fonts/ are verified 'public-asset' with permission to redistribute.")
        print("=" * 80)
        print("PUBLIC ASSET VALIDATION: PASSED")
        print("=" * 80)
        return 0

def main():
    parser = argparse.ArgumentParser(
        description="Verify that assets/fonts/ contains ONLY publicly redistributable fonts."
    )
    parser.add_argument("--catalog", default=CATALOG_PATH, help="Path to fonts.json catalog")
    parser.add_argument("--assets", default=ASSETS_FONTS_DIR, help="Path to assets/fonts directory")
    args = parser.parse_args()

    sys.exit(validate_public_release(args.catalog, args.assets))

if __name__ == "__main__":
    main()
