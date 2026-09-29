#!/usr/bin/env python3
"""
validate_licenses.py - Audit catalog fonts for commercial use, missing licenses, and embedding permissions.

Categorizes fonts into compliance tiers:
1. Permissive Open Source (OFL, Apache, MIT, CC0, Ubuntu)
2. Freeware with Commercial Grant
3. Commercial Proof Needed (Receipt / purchase required)
4. Restricted / Non-commercial Warning (Demo cut or personal use only)
5. Embedding Compliance (Checks OS/2.fsType for Office/PowerPoint distribution safety)
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not os.path.exists(os.path.join(ROOT_DIR, "catalog")):
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CATALOG = os.path.join(ROOT_DIR, "catalog", "fonts.json")

def audit_font_licenses(catalog_path: str) -> Dict[str, Any]:
    """Audit licenses across all catalog fonts."""
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    fonts = catalog.get("fonts", [])
    report = {
        "total_fonts": len(fonts),
        "open_source_count": 0,
        "commercial_count": 0,
        "redistributable_count": 0,
        "permissive_count": 0,
        "freeware_count": 0,
        "commercial_proof_needed_count": 0,
        "restricted_count": 0,
        "unknown_count": 0,
        "office_embeddable_count": 0,
        "fonts_audited": []
    }

    for f in fonts:
        fid = f.get("id")
        fname = f.get("name")
        lic = f.get("license", {})
        tech = f.get("technical", {})
        l_type = lic.get("type", "Unknown")
        comm_ok = lic.get("commercial_use", False)
        redist_ok = lic.get("redistribution_allowed", False)
        mod_ok = lic.get("modification_allowed", False)
        is_os = lic.get("open_source", False)
        vstat = lic.get("verification_status", "unknown")
        labels = lic.get("labels", [])
        risk = lic.get("risk_level", "unknown")
        fs_perm = tech.get("embedding_permission", "")

        is_office_safe = ("Installable" in fs_perm or "Editable" in fs_perm) and "Restricted" not in fs_perm

        if is_os:
            report["open_source_count"] += 1
        if comm_ok:
            report["commercial_count"] += 1
        if redist_ok:
            report["redistributable_count"] += 1

                         
        if risk == "permissive":
            report["permissive_count"] += 1
            status = "PERMISSIVE"
        elif risk == "freeware":
            report["freeware_count"] += 1
            status = "FREEWARE"
        elif risk == "commercial_proof_needed":
            report["commercial_proof_needed_count"] += 1
            status = "PROOF_NEEDED"
        elif risk == "restricted" or not comm_ok:
            report["restricted_count"] += 1
            status = "RESTRICTED"
        else:
            report["unknown_count"] += 1
            status = "UNKNOWN"

        if is_office_safe:
            report["office_embeddable_count"] += 1

        ref_files = lic.get("reference_files", [])
        has_license_file = any(
            any(k in rf.lower() for k in ["license", "ofl", "licence", "readme", "txt"])
            for rf in ref_files
        )

        report["fonts_audited"].append({
            "id": fid,
            "name": fname,
            "license_type": l_type,
            "commercial_use": comm_ok,
            "redistribution_allowed": redist_ok,
            "modification_allowed": mod_ok,
            "open_source": is_os,
            "verification_status": vstat,
            "labels": labels,
            "risk_level": risk,
            "status": status,
            "office_embeddable": is_office_safe,
            "embedding_permission": fs_perm,
            "has_license_file": has_license_file,
            "reference_files": ref_files
        })

    return report

def main():
    parser = argparse.ArgumentParser(
        description="Audit font catalog licenses for commercial use, missing documents, and embedding safety."
    )
    parser.add_argument("--catalog", default=DEFAULT_CATALOG, help="Path to fonts.json")
    parser.add_argument(
        "--filter",
        choices=["all", "issues-only", "commercial-only", "office-embeddable", "restricted", "public-safe"],
        default="all",
        help="Filter fonts displayed (default: all)"
    )
    parser.add_argument(
        "--format",
        choices=["table", "summary", "json"],
        default="table",
        help="Output format (default: table)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.catalog):
        print(f"Error: Catalog file '{args.catalog}' not found.", file=sys.stderr)
        sys.exit(1)

    report = audit_font_licenses(args.catalog)
    fonts_list = report["fonts_audited"]

    if args.filter == "issues-only":
        fonts_list = [f for f in fonts_list if f["status"] in ["RESTRICTED", "UNKNOWN", "PROOF_NEEDED"] or not f["has_license_file"]]
    elif args.filter == "commercial-only":
        fonts_list = [f for f in fonts_list if f["commercial_use"]]
    elif args.filter == "office-embeddable":
        fonts_list = [f for f in fonts_list if f["office_embeddable"]]
    elif args.filter == "restricted":
        fonts_list = [f for f in fonts_list if f["status"] == "RESTRICTED"]
    elif args.filter == "public-safe":
        fonts_list = [f for f in fonts_list if f["status"] == "PERMISSIVE"]

    if args.format == "json":
        filtered_report = dict(report)
        filtered_report["fonts_audited"] = fonts_list
        print(json.dumps(filtered_report, indent=2))
        return

    print("=" * 80)
    print("FONT LICENSE & COMMERCIAL USE AUDIT REPORT")
    print(f"• Total Families Audited:          {report['total_fonts']}")
    print(f"• Open Source Confirmed:           {report['open_source_count']} (OFL, Apache 2.0, CC0, Public Domain)")
    print(f"• Commercial Use Confirmed:        {report['commercial_count']}")
    print(f"• Publicly Redistributable:        {report['redistributable_count']}")
    print(f"• Freeware (Non-Open-Source):      {report['freeware_count']}")
    print(f"• Commercial Proof Needed:         {report['commercial_proof_needed_count']}")
    print(f"• Restricted / Demo Cut:           {report['restricted_count']}")
    print(f"• Unknown / Unclear:               {report['unknown_count']}")
    print(f"• Office / PowerPoint Embeddable:  {report['office_embeddable_count']}")
    print("-" * 80)

    if args.format == "table":
        header = f"{'ID':<18} {'OPEN SOURCE':<13} {'COMMERCIAL':<12} {'REDIST':<9} {'USER-FACING LABELS'}"
        print(header)
        print("-" * 80)
        for f in fonts_list:
            os_str = "YES" if f.get("open_source") else "NO"
            comm_str = "YES" if f["commercial_use"] else "NO / DEMO"
            redist_str = "YES" if f.get("redistribution_allowed") else "NO"
            labels_str = ", ".join(f.get("labels", []))
            print(f"{f['id'][:17]:<18} {os_str:<13} {comm_str:<12} {redist_str:<9} {labels_str}")
        print("-" * 80)
        print(f"Displayed {len(fonts_list)} of {report['total_fonts']} families (Filter: {args.filter})")

    print("=" * 80)

if __name__ == "__main__":
    main()
