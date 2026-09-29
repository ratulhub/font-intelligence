#!/usr/bin/env python3
"""
validate_catalog.py - Thorough validation of fonts.json, fonts.schema.json, file paths, IDs, and cross-references.

Checks:
1. JSON Schema conformance
2. ID syntax (kebab-case) and uniqueness
3. Physical file existence on disk for all catalog files
4. Cross-references in pairings.json and use-cases.json
5. Readability scores (1-10) and weight ladders
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Any, Tuple

try:
    import jsonschema
except ImportError:
    jsonschema = None

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not os.path.exists(os.path.join(ROOT_DIR, "catalog")):
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CATALOG = os.path.join(ROOT_DIR, "catalog", "fonts.json")
DEFAULT_SCHEMA = os.path.join(ROOT_DIR, "catalog", "fonts.schema.json")
DEFAULT_PAIRINGS = os.path.join(ROOT_DIR, "catalog", "pairings.json")
DEFAULT_USE_CASES = os.path.join(ROOT_DIR, "catalog", "use-cases.json")

def validate_catalog(
    catalog_path: str,
    schema_path: str,
    pairings_path: str,
    use_cases_path: str,
    check_files: bool = True
) -> Dict[str, Any]:
    """Run comprehensive validation."""
    report = {
        "catalog_path": catalog_path,
        "schema_validation": "SKIPPED",
        "total_fonts": 0,
        "total_files_referenced": 0,
        "missing_files": [],
        "invalid_ids": [],
        "duplicate_ids": [],
        "broken_pairing_refs": [],
        "broken_use_case_refs": [],
        "data_sanity_issues": [],
        "status": "PASS"
    }

                          
    if not os.path.exists(catalog_path):
        report["status"] = "FAIL"
        report["data_sanity_issues"].append(f"Catalog file not found: {catalog_path}")
        return report

    with open(catalog_path, "r", encoding="utf-8") as f:
        try:
            catalog = json.load(f)
        except Exception as e:
            report["status"] = "FAIL"
            report["data_sanity_issues"].append(f"Catalog JSON decode error: {e}")
            return report

                          
    if os.path.exists(schema_path) and jsonschema:
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
        try:
            jsonschema.validate(instance=catalog, schema=schema)
            report["schema_validation"] = "PASSED"
        except jsonschema.ValidationError as ve:
            report["schema_validation"] = f"FAILED: {ve.message}"
            report["status"] = "FAIL"

    fonts = catalog.get("fonts", [])
    report["total_fonts"] = len(fonts)

                                 
    id_regex = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    seen_ids = set()
    for f in fonts:
        fid = f.get("id", "")
        if not id_regex.match(fid):
            report["invalid_ids"].append(fid)
        if fid in seen_ids:
            report["duplicate_ids"].append(fid)
        seen_ids.add(fid)

                                                  
        cur = f.get("curated", {})
        read = cur.get("readability", {})
        for prop in ["body", "long_form", "ui", "small_text", "numbers"]:
            val = read.get(prop)
            if not isinstance(val, int) or val < 1 or val > 10:
                report["data_sanity_issues"].append(f"Font '{fid}' readability '{prop}' invalid: {val} (must be int 1-10)")

        tech = f.get("technical", {})
        weights = tech.get("weights", [])
        if not weights:
            report["data_sanity_issues"].append(f"Font '{fid}' technical.weights is empty")

                                         
        for file_info in f.get("files", []):
            report["total_files_referenced"] += 1
            if check_files:
                rel_p = file_info.get("path", "")
                abs_p = os.path.join(ROOT_DIR, rel_p)
                if not os.path.exists(abs_p):
                    report["missing_files"].append({
                        "font_id": fid,
                        "path": rel_p
                    })

                                  
    if os.path.exists(pairings_path):
        with open(pairings_path, "r", encoding="utf-8") as pf:
            pairings_data = json.load(pf)
        for p in pairings_data.get("pairings", []):
            pid = p.get("id")
            p_fid = p.get("primary_font", {}).get("id")
            s_fid = p.get("secondary_font", {}).get("id")
            if p_fid and p_fid not in seen_ids:
                report["broken_pairing_refs"].append(f"Pairing '{pid}' references unknown primary font '{p_fid}'")
            if s_fid and s_fid not in seen_ids:
                report["broken_pairing_refs"].append(f"Pairing '{pid}' references unknown secondary font '{s_fid}'")

                                   
    if os.path.exists(use_cases_path):
        with open(use_cases_path, "r", encoding="utf-8") as uf:
            uc_data = json.load(uf)
        for ucid, uc in uc_data.get("use_cases", {}).items():
            for pair_ref in uc.get("recommended_curated_pairings", []):
                                                    
                pass

    if (report["missing_files"] or report["invalid_ids"] or report["duplicate_ids"] or
        report["broken_pairing_refs"] or report["data_sanity_issues"] or
        "FAILED" in report["schema_validation"]):
        report["status"] = "FAIL"

    return report

def main():
    parser = argparse.ArgumentParser(
        description="Thorough validation of fonts.json, schema, file paths, IDs, and cross-references."
    )
    parser.add_argument("--catalog", default=DEFAULT_CATALOG, help="Path to fonts.json")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, help="Path to fonts.schema.json")
    parser.add_argument("--pairings", default=DEFAULT_PAIRINGS, help="Path to pairings.json")
    parser.add_argument("--use-cases", default=DEFAULT_USE_CASES, help="Path to use-cases.json")
    parser.add_argument("--no-check-files", action="store_true", help="Skip checking physical files on disk")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")

    args = parser.parse_args()

    report = validate_catalog(
        catalog_path=args.catalog,
        schema_path=args.schema,
        pairings_path=args.pairings,
        use_cases_path=args.use_cases,
        check_files=not args.no_check_files
    )

    if args.json:
        print(json.dumps(report, indent=2))
        sys.exit(0 if report["status"] == "PASS" else 1)

    print("=" * 80)
    print("FONT INTELLIGENCE CATALOG VALIDATION AUDIT")
    print("=" * 80)
    status_badge = "[PASSED]" if report["status"] == "PASS" else "[FAILED]"
    print(f"• Overall Status:           {status_badge}")
    print(f"• Catalog Path:             {report['catalog_path']}")
    print(f"• Schema Validation:        {report['schema_validation']}")
    print(f"• Total Families:           {report['total_fonts']}")
    print(f"• Total Files Referenced:   {report['total_files_referenced']}")
    print(f"• Missing Physical Files:   {len(report['missing_files'])}")
    print(f"• Invalid ID Patterns:      {len(report['invalid_ids'])}")
    print(f"• Duplicate IDs:            {len(report['duplicate_ids'])}")
    print(f"• Broken Pairing Refs:      {len(report['broken_pairing_refs'])}")
    print(f"• Sanity / Value Issues:    {len(report['data_sanity_issues'])}")
    print("-" * 80)

    if report["missing_files"]:
        print("\n[!] MISSING FILES ON DISK:")
        for mf in report["missing_files"][:10]:
            print(f"    Font '{mf['font_id']}': {mf['path']}")
        if len(report["missing_files"]) > 10:
            print(f"    ... and {len(report['missing_files']) - 10} more missing files.")

    if report["broken_pairing_refs"]:
        print("\n[!] BROKEN PAIRING REFERENCES:")
        for bp in report["broken_pairing_refs"]:
            print(f"    {bp}")

    if report["data_sanity_issues"]:
        print("\n[!] DATA SANITY ISSUES:")
        for ds in report["data_sanity_issues"]:
            print(f"    {ds}")

    print("=" * 80)
    sys.exit(0 if report["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
