#!/usr/bin/env python3
"""
build_release_manifest.py - Generate Release Manifest and Manage Public Assets

Generates release manifests separating public-asset and catalog-only fonts:
- docs/public-assets-manifest.md
- docs/release-manifest.json

Options:
  --sync-assets    Synchronize assets/fonts/ with verified public-asset fonts only.
  --dry-run        Print actions without modifying assets/fonts/.
"""

import sys
import os
import json
import shutil
import hashlib
import argparse
from typing import Dict, List, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
ASSETS_FONTS_DIR = os.path.join(ROOT_DIR, "assets", "fonts")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
MANIFEST_MD_PATH = os.path.join(DOCS_DIR, "public-assets-manifest.md")
MANIFEST_JSON_PATH = os.path.join(DOCS_DIR, "release-manifest.json")

def compute_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(catalog_path: str = CATALOG_PATH, sync_assets: bool = False, dry_run: bool = False) -> Dict[str, Any]:
    print("=" * 80)
    print("FONT INTELLIGENCE: RELEASE MANIFEST & ASSET AUDITOR")
    print("=" * 80)

    if not os.path.exists(catalog_path):
        print(f"[FAIL] Catalog not found: {catalog_path}")
        sys.exit(1)

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    fonts = catalog.get("fonts", [])
    total_families = len(fonts)
    print(f"• Total Catalog Families:          {total_families}")

    public_assets = []
    catalog_only = []
    restricted = []
    unknown = []

    license_counts: Dict[str, int] = {}

    for f in fonts:
        dist = f.get("distribution_status", "unknown")
        lic_type = f.get("license", {}).get("type", "Unknown")
        license_counts[lic_type] = license_counts.get(lic_type, 0) + 1

        entry_summary = {
            "id": f["id"],
            "name": f["name"],
            "license": lic_type,
            "commercial_use": f.get("license", {}).get("commercial_use", False),
            "redistribution_allowed": f.get("license", {}).get("redistribution_allowed", False),
            "files": [
                {
                    "path": fl["path"],
                    "format": fl.get("format"),
                    "weight": fl.get("weight"),
                    "sha256": fl.get("sha256")
                }
                for fl in f.get("files", [])
            ]
        }

        if dist == "public-asset":
            public_assets.append(entry_summary)
        elif dist == "restricted":
            restricted.append(entry_summary)
        elif dist == "catalog-only":
            catalog_only.append(entry_summary)
        else:
            unknown.append(entry_summary)

    print(f"• Public Asset Families:           {len(public_assets)}")
    print(f"• Catalog-Only Families:           {len(catalog_only)}")
    print(f"• Restricted Families:             {len(restricted)}")
    print(f"• Unknown Distribution Families:   {len(unknown)}")

                                                         
    if sync_assets:
        print("\n" + "-" * 80)
        print("SYNCHRONIZING assets/fonts/ DIRECTORY...")
        os.makedirs(ASSETS_FONTS_DIR, exist_ok=True)
        current_in_assets = set(os.listdir(ASSETS_FONTS_DIR))
        allowed_ids = {p["id"] for p in public_assets}

                                                     
        to_remove = current_in_assets - allowed_ids
        for r_id in sorted(list(to_remove)):
            r_path = os.path.join(ASSETS_FONTS_DIR, r_id)
            if os.path.isdir(r_path):
                print(f"  [-] PURGING restricted/catalog-only folder from assets/fonts/: {r_id}")
                if not dry_run:
                    shutil.rmtree(r_path)

                                      
        to_add = allowed_ids - current_in_assets
        for a_id in sorted(list(to_add)):
                                           
            f_entry = next(f for f in fonts if f["id"] == a_id)
            dest_dir = os.path.join(ASSETS_FONTS_DIR, a_id)
            print(f"  [+] COPYING public-asset to assets/fonts/: {a_id}")
            if not dry_run:
                os.makedirs(dest_dir, exist_ok=True)
                for fl in f_entry.get("files", []):
                    src_p = os.path.join(ROOT_DIR, fl["path"])
                    if os.path.exists(src_p):
                        shutil.copy2(src_p, dest_dir)
                for ref in f_entry.get("license", {}).get("reference_files", []):
                    src_ref = os.path.join(ROOT_DIR, ref)
                    if os.path.exists(src_ref):
                        shutil.copy2(src_ref, dest_dir)

                                 
    total_public_binaries = sum(len(p["files"]) for p in public_assets)
    total_catalog_binaries = sum(len(f.get("files", [])) for f in fonts)

    manifest_data = {
        "generated_at": catalog.get("generated_at"),
        "version": catalog.get("version"),
        "counts": {
            "total_families": total_families,
            "public_asset_families": len(public_assets),
            "catalog_only_families": len(catalog_only),
            "restricted_families": len(restricted),
            "unknown_families": len(unknown),
            "total_catalog_binaries": total_catalog_binaries,
            "total_public_binaries": total_public_binaries
        },
        "license_distribution": license_counts,
        "public_assets": public_assets,
        "catalog_only": [{"id": c["id"], "name": c["name"], "license": c["license"]} for c in catalog_only],
        "restricted": [{"id": r["id"], "name": r["name"], "license": r["license"]} for r in restricted],
        "unknown": [{"id": u["id"], "name": u["name"], "license": u["license"]} for u in unknown]
    }

                        
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(MANIFEST_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"\n• Generated JSON Manifest:         {os.path.relpath(MANIFEST_JSON_PATH, ROOT_DIR)}")

                            
    with open(MANIFEST_MD_PATH, "w", encoding="utf-8") as f:
        f.write("# Font Intelligence - Public Assets Release Manifest\n\n")
        f.write("This manifest documents all fonts approved for open redistribution in the `assets/fonts/` directory.\n\n")
        f.write("## Summary Metrics\n\n")
        f.write(f"- **Total Catalog Families**: {total_families}\n")
        f.write(f"- **Publicly Redistributable Families**: {len(public_assets)}\n")
        f.write(f"- **Catalog-Only / Restricted Families**: {len(catalog_only) + len(restricted) + len(unknown)}\n")
        f.write(f"- **Public Binaries**: {total_public_binaries}\n\n")
        f.write("## Public Asset Families (Included in `assets/fonts/`)\n\n")
        f.write("| Family ID | Font Name | License | Commercial Use | Redistribution | Binaries |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: |\n")
        for p in public_assets:
            f.write(f"| `{p['id']}` | **{p['name']}** | {p['license']} | {'Yes' if p['commercial_use'] else 'No'} | {'Allowed' if p['redistribution_allowed'] else 'Blocked'} | {len(p['files'])} |\n")
        f.write("\n## Catalog-Only & Non-Redistributable Families\n\n")
        f.write("These families are indexed in `catalog/fonts.json` for AI reasoning, CSS styling, and local rendering, but raw binaries are NOT distributed in `assets/fonts/`:\n\n")
        f.write("| Family ID | Font Name | License | Classification |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for c in catalog_only:
            f.write(f"| `{c['id']}` | {c['name']} | {c['license']} | Catalog Only |\n")
        for r in restricted:
            f.write(f"| `{r['id']}` | {r['name']} | {r['license']} | Restricted (Evaluation/Non-Commercial) |\n")
        for u in unknown:
            f.write(f"| `{u['id']}` | {u['name']} | {u['license']} | Unknown / Pending Review |\n")

    print(f"• Generated Markdown Manifest:     {os.path.relpath(MANIFEST_MD_PATH, ROOT_DIR)}")
    print("=" * 80)
    print("MANIFEST GENERATION COMPLETE")
    print("=" * 80)
    return manifest_data

def main():
    parser = argparse.ArgumentParser(description="Build Font Intelligence release manifests.")
    parser.add_argument("--sync-assets", action="store_true", help="Synchronize assets/fonts/ with public-asset fonts")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry-run without writing to assets/fonts/")
    parser.add_argument("--catalog", default=CATALOG_PATH, help="Path to fonts.json")
    args = parser.parse_args()

    build_manifest(args.catalog, args.sync_assets, args.dry_run)

if __name__ == "__main__":
    main()
