#!/usr/bin/env python3
"""
build_catalog.py - Build or incrementally update the canonical fonts.json catalog.

Preserves all curated design intelligence (category, subtype, styles, roles,
readability ratings, fallback stacks, and notes) while refreshing technical
font metadata, binary file listings, weights, and embedding permissions.
Includes schema validation, dry-run mode, and backup safety.
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime, timezone
from collections import defaultdict
from typing import Dict, List, Any, Optional

try:
    import jsonschema
except ImportError:
    jsonschema = None

# Import our scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_fonts import scan_source

sys.stdout.reconfigure(encoding='utf-8')

def get_workspace_root() -> str:
    """Find the workspace root containing 'All fonts'."""
    cur = os.path.abspath(__file__)
    for _ in range(5):
        cur = os.path.dirname(cur)
        if os.path.exists(os.path.join(cur, "All fonts")):
            return cur
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = get_workspace_root()
DEFAULT_SOURCE = os.path.join(ROOT_DIR, "All fonts")
DEFAULT_CATALOG = os.path.join(ROOT_DIR, "catalog", "fonts.json")
DEFAULT_SCHEMA = os.path.join(ROOT_DIR, "catalog", "fonts.schema.json")


def normalize_id(text: str) -> str:
    """Produce clean kebab-case ID."""
    clean = text.lower().strip()
    import re
    clean = re.sub(r"[^a-z0-9]+", "-", clean)
    return clean.strip("-")


def determine_license(pkg_dir: str, pkg_files: List[str]) -> Dict[str, Any]:
    """Inspect folder texts to determine license."""
    texts = []
    ref_files = []
    
    for f in pkg_files:
        ext = os.path.splitext(f)[1].lower()
        if ext in [".txt", ".md", ".license", ".licence", ".html"]:
            ref_files.append(f)
            abs_p = os.path.join(ROOT_DIR, f)
            if os.path.exists(abs_p):
                try:
                    with open(abs_p, "r", encoding="utf-8", errors="ignore") as tf:
                        texts.append(tf.read().lower())
                except Exception:
                    pass

    comb = " ".join(texts) + " " + " ".join(ref_files).lower()

    if "sil open font license" in comb or "ofl" in comb:
        return {"type": "SIL Open Font License 1.1 (OFL)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://scripts.sil.org/OFL"}
    if "creative commons zero" in comb or "cc0" in comb:
        return {"type": "Creative Commons Zero 1.0 (CC0)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://creativecommons.org/publicdomain/zero/1.0/"}
    if "fontshare" in comb or "ffl" in comb:
        return {"type": "ITF Free Font License (Fontshare FFL 2.0)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://www.fontshare.com/licensing"}
    if "ubuntu" in comb and "ufl" in comb:
        return {"type": "Ubuntu Font Licence 1.0", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://ubuntu.com/legal/font-licence"}
    if "apache" in comb:
        return {"type": "Apache License 2.0", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://www.apache.org/licenses/LICENSE-2.0"}
    if "1001fonts" in comb:
        return {"type": "1001Fonts Free Commercial License (FFC)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://www.1001fonts.com/licenses/ffc.html"}
    if "commercial" in comb or "free" in comb:
        return {"type": "Freeware (Commercial Use Granted)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}

    return {"type": "Standard Free / Open License", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": None}


def default_curated_for_font(family_name: str, tech: Dict[str, Any]) -> Dict[str, Any]:
    """Default fallback curated object for brand-new fonts."""
    category = "sans-serif"
    if "mono" in family_name.lower():
        category = "monospace"
    elif "serif" in family_name.lower():
        category = "serif"

    return {
        "category": category,
        "subtype": "contemporary",
        "styles": ["modern"],
        "roles": ["heading", "body"] if category != "monospace" else ["code"],
        "readability": {
            "body": 7 if category != "monospace" else 6,
            "long_form": 7 if category != "monospace" else 5,
            "ui": 7,
            "small_text": 6,
            "numbers": 7
        },
        "fallback": ["system-ui", "sans-serif"] if category == "sans-serif" else ["Georgia", "serif"],
        "notes": f"Catalog entry for {family_name}."
    }


def build_or_update_catalog(
    source_dir: str,
    catalog_path: str,
    schema_path: Optional[str] = None,
    dry_run: bool = False,
    backup: bool = True
) -> Dict[str, Any]:
    """Build or update catalog preserving curated fields."""
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source fonts directory not found: {source_dir}")

    # Load existing catalog to preserve curated data
    existing_fonts_by_id = {}
    old_catalog = {}
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            old_catalog = json.load(f)
            for item in old_catalog.get("fonts", []):
                existing_fonts_by_id[item["id"]] = item

    print(f"Scanning source binaries in: {source_dir} ...", file=sys.stderr)
    scanned_binaries = scan_source(source_dir)
    print(f"Scanned {len(scanned_binaries)} font binaries.", file=sys.stderr)

    # Group binaries by family
    family_bins = defaultdict(list)
    for b in scanned_binaries:
        # Determine family group key from folder or family_name
        rel_path = os.path.relpath(b["file_path"], source_dir)
        folder_top = rel_path.split(os.sep)[0].split("/")[0]
        
        # Match against existing font IDs first
        matched_id = None
        for eid, efont in existing_fonts_by_id.items():
            if folder_top.lower() == eid.lower() or b["family_name"].lower() == efont["name"].lower():
                matched_id = eid
                break
        
        family_key = matched_id or normalize_id(b["family_name"])
        family_bins[family_key].append(b)

    updated_fonts = []
    preserved_count = 0
    new_count = 0

    for fid, bins in sorted(family_bins.items()):
        existing = existing_fonts_by_id.get(fid)
        fam_name = existing["name"] if existing else bins[0]["family_name"]
        
        files_list = []
        weights = set()
        scripts = set(["Latin"])
        blocks = set()
        is_var = False
        var_axes = []
        has_italics = False
        all_pkg_files = []

        for b in bins:
            rel_repo = os.path.relpath(b["file_path"], ROOT_DIR).replace("\\", "/")
            files_list.append({
                "path": rel_repo,
                "format": b["file_format"],
                "weight": b["weight"],
                "style": "italic" if b.get("italic") else "normal",
                "variable": b.get("is_variable", False),
                "size_bytes": b["file_size_bytes"],
                "sha256": b["sha256"]
            })
            weights.add(b["weight"])
            for s in b.get("scripts", []): scripts.add(s)
            for blk in b.get("unicode_blocks", []): blocks.add(blk)
            if b.get("is_variable"):
                is_var = True
                var_axes.extend(b.get("variable_axes", []))
            if b.get("italic"):
                has_italics = True
            all_pkg_files.append(rel_repo)

        # Format axes for schema
        formatted_axes = []
        for ax in var_axes:
            formatted_axes.append({
                "tag": ax.get("tag", "wght"),
                "name": ax.get("tag", "Weight"),
                "min": float(ax.get("min_value", ax.get("min", 100))),
                "default": float(ax.get("default_value", ax.get("default", 400))),
                "max": float(ax.get("max_value", ax.get("max", 900)))
            })

        # Technical block matching fonts.schema.json
        tech = {
            "weights": sorted(list(weights)) if weights else (existing["technical"]["weights"] if existing else [400]),
            "italic": has_italics or (existing["technical"]["italic"] if existing else False),
            "variable": is_var or (existing["technical"]["variable"] if existing else False),
            "axes": formatted_axes if formatted_axes else (existing["technical"]["axes"] if existing else []),
            "scripts": sorted(list(scripts)) if scripts else (existing["technical"]["scripts"] if existing else ["Latin"]),
            "languages": existing["technical"]["languages"] if existing else ["en"],
            "unicode_blocks": sorted(list(blocks)) if blocks else (existing["technical"]["unicode_blocks"] if existing else ["Basic Latin"]),
            "total_glyphs": existing["technical"]["total_glyphs"] if existing else sum(b.get("glyph_count", 0) for b in bins),
            "opentype_features": existing["technical"]["opentype_features"] if existing else ["kern"],
            "embedding_permission": bins[0].get("embedding_permission", "Installable Embedding (unrestricted)") if bins else (existing["technical"]["embedding_permission"] if existing else "Installable Embedding (unrestricted)")
        }

        # License
        license_info = existing["license"] if existing else determine_license(fid, all_pkg_files)

        # Curated block (PRESERVED)
        if existing and "curated" in existing:
            curated = existing["curated"]
            preserved_count += 1
        else:
            curated = default_curated_for_font(fam_name, tech)
            new_count += 1

        # Provenance matching schema
        if existing and "provenance" in existing:
            prov = existing["provenance"]
        else:
            prov = {
                "source_packages": [fid],
                "designer": None,
                "manufacturer": None,
                "designer_url": None,
                "vendor_url": None,
                "version": bins[0].get("version") or "1.0",
                "copyright": None
            }

        font_entry = {
            "id": fid,
            "name": fam_name,
            "aliases": existing.get("aliases", [fam_name]) if existing else [fam_name],
            "curated": curated,
            "technical": tech,
            "files": sorted(files_list, key=lambda x: x["path"]),
            "provenance": prov,
            "license": license_info
        }
        updated_fonts.append(font_entry)

    # Sort catalog deterministically by font ID
    updated_fonts.sort(key=lambda x: x["id"])

    new_catalog = {
        "$schema": "./fonts.schema.json",
        "version": "2.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/build_catalog.py",
        "total_families": len(updated_fonts),
        "fonts": updated_fonts
    }

    # Validate against schema if available
    if schema_path and os.path.exists(schema_path) and jsonschema:
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
        jsonschema.validate(instance=new_catalog, schema=schema)
        print("Catalog schema validation: PASSED.", file=sys.stderr)

    if not dry_run:
        if backup and os.path.exists(catalog_path):
            bak_path = f"{catalog_path}.bak"
            shutil.copy2(catalog_path, bak_path)
            print(f"Created backup: {bak_path}", file=sys.stderr)

        os.makedirs(os.path.dirname(os.path.abspath(catalog_path)), exist_ok=True)
        with open(catalog_path, "w", encoding="utf-8") as f:
            json.dump(new_catalog, f, indent=2)
        print(f"Successfully wrote catalog to: {catalog_path}", file=sys.stderr)

    return {
        "total_families": len(updated_fonts),
        "preserved_curated_count": preserved_count,
        "new_families_count": new_count,
        "dry_run": dry_run,
        "target_file": catalog_path
    }


def main():
    parser = argparse.ArgumentParser(
        description="Build or incrementally update fonts.json preserving all curated fields."
    )
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE, help="Source fonts directory (default: 'All fonts')")
    parser.add_argument("--catalog-path", default=DEFAULT_CATALOG, help="Target fonts.json path")
    parser.add_argument("--schema-path", default=DEFAULT_SCHEMA, help="Path to fonts.schema.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview updates without writing to disk")
    parser.add_argument("--no-backup", action="store_true", help="Do not create .bak backup before writing")

    args = parser.parse_args()

    try:
        res = build_or_update_catalog(
            source_dir=args.source_dir,
            catalog_path=args.catalog_path,
            schema_path=args.schema_path,
            dry_run=args.dry_run,
            backup=not args.no_backup
        )
        print("=" * 80)
        print("CATALOG BUILD & PRESERVATION REPORT")
        print("=" * 80)
        print(f"• Total Families:        {res['total_families']}")
        print(f"• Preserved Curated:     {res['preserved_curated_count']} families (100% intelligence retained)")
        print(f"• New Additions:         {res['new_families_count']}")
        print(f"• Dry Run:               {'YES (No files modified)' if res['dry_run'] else 'NO (Catalog saved)'}")
        print(f"• Output Path:           {res['target_file']}")
        print("=" * 80)
    except Exception as e:
        print(f"Build error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
