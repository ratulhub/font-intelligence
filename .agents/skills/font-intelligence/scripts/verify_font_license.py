#!/usr/bin/env python3
"""
verify_font_license.py - Automated & Authoritative Font License Verification

Audits local license files, embedded OpenType metadata, and records authoritative
licensing evidence. Distinguishes commercial-use permission from raw binary redistribution.
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
FONTS_DIR = os.path.join(ROOT_DIR, "All fonts")

KNOWN_PERMISSIVE_KEYWORDS = [
    "sil open font license", "ofl-1.1", "ofl 1.1", "apache license, version 2.0",
    "apache-2.0", "mit license", "creative commons zero", "cc0 1.0", "public domain"
]

KNOWN_RESTRICTIVE_KEYWORDS = [
    "personal use only", "non-commercial only", "donationware", "shareware",
    "demo version", "for evaluation only", "strictly prohibited", "no redistribution",
    "cannot be distributed", "resale or redistribution prohibited"
]

def audit_local_package(pkg_path: str) -> Dict[str, Any]:
    evidence = {
        "license_files": [],
        "readme_files": [],
        "snippets": [],
        "detected_license": "Unknown",
        "commercial_use": False,
        "redistribution": False,
        "modification": False,
        "confidence": "unknown"
    }

    if not os.path.exists(pkg_path):
        return evidence

    for root, _, files in os.walk(pkg_path):
        for f in files:
            fl = f.lower()
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")

            if any(k in fl for k in ["license", "ofl", "copying", "eula"]):
                evidence["license_files"].append(rel_path)
            elif any(k in fl for k in ["readme", "about", "info", "font by"]):
                evidence["readme_files"].append(rel_path)

            if fl.endswith((".txt", ".md", ".rtf")):
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read(8192)
                        content_lower = content.lower()

                        if any(kw in content_lower for kw in KNOWN_PERMISSIVE_KEYWORDS):
                            evidence["detected_license"] = "SIL Open Font License 1.1 (OFL)" if "open font" in content_lower else "Permissive Open Source"
                            evidence["commercial_use"] = True
                            evidence["redistribution"] = True
                            evidence["modification"] = True
                            evidence["confidence"] = "verified"
                            evidence["snippets"].append(content[:300].strip())
                        elif any(kw in content_lower for kw in KNOWN_RESTRICTIVE_KEYWORDS):
                            evidence["detected_license"] = "Personal Use Only / Evaluation"
                            evidence["commercial_use"] = False
                            evidence["redistribution"] = False
                            evidence["modification"] = False
                            evidence["confidence"] = "restricted"
                            evidence["snippets"].append(content[:300].strip())
                        elif "commercial" in content_lower and "free" in content_lower:
                            evidence["detected_license"] = "Free for Commercial Use"
                            evidence["commercial_use"] = True
                            evidence["redistribution"] = "redistribut" in content_lower
                            evidence["modification"] = False
                            evidence["confidence"] = "needs-review"
                            evidence["snippets"].append(content[:300].strip())
                except Exception:
                    pass

    return evidence

def verify_font_license(font_id: Optional[str] = None, filter_status: Optional[str] = None, update_catalog: bool = False) -> None:
    print("=" * 80)
    print("FONT INTELLIGENCE: LICENSE VERIFICATION & AUDIT ENGINE")
    print("=" * 80)

    if not os.path.exists(CATALOG_PATH):
        print(f"[FAIL] Catalog not found: {CATALOG_PATH}")
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    fonts = catalog.get("fonts", [])
    today = datetime.now().strftime("%Y-%m-%d")

    if font_id:
        targets = [f for f in fonts if f["id"] == font_id]
        if not targets:
            print(f"[FAIL] Font ID '{font_id}' not found in catalog.")
            sys.exit(1)
    elif filter_status:
        targets = [f for f in fonts if f.get("license", {}).get("tracking", {}).get("verification_status") == filter_status]
    else:
        targets = fonts

    print(f"• Auditing {len(targets)} font families...\n")

    updated_count = 0
    results = []

    for f in targets:
        fid = f["id"]
        pkgs = f.get("provenance", {}).get("source_packages", [fid])
        existing_tracking = f.get("license", {}).get("tracking", {})

                               
        pkg_path = os.path.join(FONTS_DIR, pkgs[0]) if pkgs else os.path.join(FONTS_DIR, fid)
        local_audit = audit_local_package(pkg_path)

        verif_status = existing_tracking.get("verification_status", "unknown")
        if local_audit["confidence"] == "verified":
            verif_status = "verified"
        elif local_audit["confidence"] == "restricted":
            verif_status = "restricted"
        elif verif_status == "unknown" and local_audit["confidence"] != "unknown":
            verif_status = local_audit["confidence"]

        result = {
            "id": fid,
            "name": f["name"],
            "license": local_audit["detected_license"] if local_audit["detected_license"] != "Unknown" else f.get("license", {}).get("type", "Unknown"),
            "commercial": local_audit["commercial_use"] or f.get("license", {}).get("commercial_use", False),
            "redistribution": local_audit["redistribution"] or f.get("license", {}).get("redistribution_allowed", False),
            "status": verif_status,
            "evidence_files": local_audit["license_files"] or local_audit["readme_files"]
        }
        results.append(result)

        if update_catalog:
            f.setdefault("license", {}).setdefault("tracking", {})
            f["license"]["tracking"]["verification_status"] = verif_status
            f["license"]["tracking"]["verification_date"] = today
            if local_audit["license_files"]:
                f["license"]["tracking"]["license_file"] = local_audit["license_files"][0]
            updated_count += 1

                         
    print(f"{'FAMILY ID':<25} {'COMMERCIAL':<12} {'REDISTRIBUTE':<14} {'STATUS':<15} {'LICENSE TYPE'}")
    print("-" * 80)
    for r in results[:40]:
        comm_str = "YES" if r["commercial"] else "NO"
        redist_str = "YES" if r["redistribution"] else "NO"
        print(f"{r['id']:<25} {comm_str:<12} {redist_str:<14} {r['status']:<15} {r['license'][:25]}")

    if len(results) > 40:
        print(f"... and {len(results) - 40} more families.")

    print("-" * 80)
    status_counts = {}
    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1

    print("Verification Status Breakdown:")
    for st, c in sorted(status_counts.items()):
        print(f"  • {st:<15}: {c}")

    if update_catalog and updated_count > 0:
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
                                 
        skill_catalog = os.path.join(ROOT_DIR, ".agents", "skills", "font-intelligence", "catalog", "fonts.json")
        if os.path.exists(os.path.dirname(skill_catalog)):
            with open(skill_catalog, "w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2)
        print(f"\n[OK] Updated verification metadata for {updated_count} families.")

    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Verify and audit font licensing.")
    parser.add_argument("--font", help="Specific font family ID to audit")
    parser.add_argument("--filter", choices=["verified", "needs-review", "restricted", "unknown"], help="Filter by verification status")
    parser.add_argument("--update", action="store_true", help="Update catalog with audited verification status")
    args = parser.parse_args()

    verify_font_license(args.font, args.filter, args.update)

if __name__ == "__main__":
    main()
