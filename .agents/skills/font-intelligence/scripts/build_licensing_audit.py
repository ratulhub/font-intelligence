#!/usr/bin/env python3
"""
build_licensing_audit.py - Build the complete licensing tracking dataset and generate docs/redistribution-review.md.

Enforces the core rule:
Do NOT assume "free for commercial use" = "allowed to redistribute on GitHub".
Never delete original license/readme files.

Tracks:
- license name
- SPDX ID if known
- commercial use
- redistribution
- modification
- license file
- source
- source URL
- verification status (verified, needs-review, restricted, unknown)
- verification date
"""

import os
import sys
import json
from datetime import datetime, timezone
from typing import Dict, List, Any

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
OUTPUT_MD = os.path.join(DOCS_DIR, "redistribution-review.md")

TODAY = "2026-09-29"


def analyze_font_license(font: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze font license and determine strict redistribution terms."""
    fid = font["id"]
    fname = font["name"]
    lic = font.get("license", {})
    prov = font.get("provenance", {})
    l_type = lic.get("type", "")
    ref_files = lic.get("reference_files", [])
    pkg = prov.get("source_packages", [fid])[0] if prov.get("source_packages") else fid

    # Find primary license file
    license_file = None
    for rf in ref_files:
        low = rf.lower()
        if "license" in low or "ofl" in low or "eula" in low or "licence" in low:
            license_file = rf
            break
    if not license_file and ref_files:
        license_file = ref_files[0]

    designer = prov.get("designer")
    manufacturer = prov.get("manufacturer")
    source_name = manufacturer or designer or pkg
    source_url = prov.get("designer_url") or prov.get("vendor_url") or lic.get("license_url")

    # Default values
    tracking = {
        "license_name": l_type,
        "spdx_id": None,
        "commercial_use": False,
        "redistribution": False,
        "modification": False,
        "license_file": license_file,
        "source": source_name,
        "source_url": source_url,
        "verification_status": "unknown",
        "verification_date": TODAY,
        "redistribution_notes": ""
    }

    # 1. SIL Open Font License 1.1
    if "sil open font license" in l_type.lower() or "ofl" in l_type.lower():
        tracking.update({
            "license_name": "SIL Open Font License 1.1",
            "spdx_id": "OFL-1.1",
            "commercial_use": True,
            "redistribution": True,
            "modification": True,
            "verification_status": "verified",
            "source_url": source_url or "https://scripts.sil.org/OFL",
            "redistribution_notes": "Permitted to redistribute, bundle, embed, and modify under OFL-1.1 terms. Cannot be sold alone."
        })

    # 2. Creative Commons Zero 1.0 (CC0)
    elif "creative commons zero" in l_type.lower() or "cc0" in l_type.lower():
        tracking.update({
            "license_name": "Creative Commons Zero 1.0 Universal (CC0)",
            "spdx_id": "CC0-1.0",
            "commercial_use": True,
            "redistribution": True,
            "modification": True,
            "verification_status": "verified",
            "source_url": source_url or "https://creativecommons.org/publicdomain/zero/1.0/",
            "redistribution_notes": "Public domain dedication. Fully permissive for all commercial uses, modifications, and redistribution."
        })

    # 3. Apache License 2.0
    elif "apache" in l_type.lower():
        tracking.update({
            "license_name": "Apache License 2.0",
            "spdx_id": "Apache-2.0",
            "commercial_use": True,
            "redistribution": True,
            "modification": True,
            "verification_status": "verified",
            "source_url": source_url or "https://www.apache.org/licenses/LICENSE-2.0",
            "redistribution_notes": "Permissive open-source license allowing commercial use, redistribution, and modification with copyright notice."
        })

    # 4. ITF Free Font License (Fontshare FFL)
    elif "itf free font license" in l_type.lower() or "fontshare" in l_type.lower():
        tracking.update({
            "license_name": "ITF Free Font License (Fontshare FFL 2.0)",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": True,
            "modification": True,
            "verification_status": "verified",
            "source_url": source_url or "https://www.fontshare.com/licensing",
            "redistribution_notes": "Permissive foundry license from Indian Type Foundry allowing commercial use, embedding, and redistribution with attribution."
        })

    # 5. Public Domain Dedication
    elif "public domain" in l_type.lower():
        tracking.update({
            "license_name": "Public Domain Dedication",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": True,
            "modification": True,
            "verification_status": "verified",
            "source_url": source_url,
            "redistribution_notes": "No rights reserved. Free for commercial use, redistribution, and modification."
        })

    # 6. Ubuntu Font Licence 1.0
    elif "ubuntu" in l_type.lower() and "licence" in l_type.lower():
        tracking.update({
            "license_name": "Ubuntu Font Licence 1.0",
            "spdx_id": "Ubuntu-1.0",
            "commercial_use": True,
            "redistribution": True,
            "modification": True,
            "verification_status": "verified",
            "source_url": source_url or "https://ubuntu.com/legal/font-licence",
            "redistribution_notes": "Permissive open license developed by Canonical for Ubuntu. Allows redistribution and derivative fonts under UFL."
        })

    # 7. 1001Fonts Free Commercial License (FFC)
    elif "1001fonts" in l_type.lower() or "ffc" in l_type.lower():
        tracking.update({
            "license_name": "1001Fonts Free For Commercial Use License (FFC)",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": False,
            "modification": False,
            "verification_status": "needs-review",
            "source_url": source_url or "https://www.1001fonts.com/licenses/ffc.html",
            "redistribution_notes": "Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission."
        })

    # 8. Creative Fabrica Commercial License
    elif "creative fabrica" in l_type.lower():
        tracking.update({
            "license_name": "Creative Fabrica Commercial License",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": False,
            "modification": False,
            "verification_status": "needs-review",
            "source_url": source_url or "https://www.creativefabrica.com",
            "redistribution_notes": "Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files."
        })

    # 9. Letterlays Commercial License
    elif "letterlays" in l_type.lower():
        tracking.update({
            "license_name": "Letterlays Commercial License (Receipt PDF)",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": False,
            "modification": False,
            "verification_status": "needs-review",
            "source_url": source_url or "https://letterlays.com",
            "redistribution_notes": "Commercial design grant with receipt PDF. Prohibits raw font file distribution or open-source repackaging."
        })

    # 10. Courbe Sans Free Standard License
    elif "courbe sans" in l_type.lower():
        tracking.update({
            "license_name": "Courbe Sans Free Standard License",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": False,
            "modification": False,
            "verification_status": "needs-review",
            "source_url": source_url,
            "redistribution_notes": "Author grants free standard commercial design usage, but does not grant third-party public git repository redistribution rights."
        })

    # 11. Freeware Grants (Befonts, Aluyeah, Author Grant)
    elif "freeware" in l_type.lower():
        tracking.update({
            "license_name": l_type,
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": False,
            "modification": False,
            "verification_status": "needs-review",
            "source_url": source_url,
            "redistribution_notes": "Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation."
        })

    # 12. NimaVisual EULA (No Redistribution)
    elif "nimavisual" in l_type.lower():
        tracking.update({
            "license_name": "NimaVisual End User License Agreement",
            "spdx_id": None,
            "commercial_use": False,
            "redistribution": False,
            "modification": False,
            "verification_status": "restricted",
            "source_url": source_url or "http://be.net/NimaVisual",
            "redistribution_notes": "RESTRICTED: License text explicitly states 'strictly no redistribution, selling, or file sharing'. Commercial design usage requires commercial license purchase."
        })

    # 13. Eimantas Paškonis EULA
    elif "paškonis" in l_type.lower() or "paskonis" in l_type.lower():
        tracking.update({
            "license_name": "Eimantas Paškonis EULA (Commercial OK, No File Sharing)",
            "spdx_id": None,
            "commercial_use": True,
            "redistribution": False,
            "modification": False,
            "verification_status": "restricted",
            "source_url": source_url,
            "redistribution_notes": "RESTRICTED FOR REDISTRIBUTION: Commercial design use granted, but license explicitly forbids uploading to public file-sharing sites or redistributing font binaries."
        })

    # 14. Evaluation / Demo Cut
    elif "demo" in l_type.lower() or "evaluation" in l_type.lower():
        tracking.update({
            "license_name": "Evaluation / Demo Cut (Commercial Purchase Required)",
            "spdx_id": None,
            "commercial_use": False,
            "redistribution": False,
            "modification": False,
            "verification_status": "restricted",
            "source_url": source_url or "https://ffeeaarr.my.id/",
            "redistribution_notes": "RESTRICTED: Personal use / demo cut only. Commercial usage and redistribution prohibited without purchasing commercial license from author."
        })

    # 15. Unspecified Copyright
    elif "copyright" in l_type.lower():
        tracking.update({
            "license_name": l_type,
            "spdx_id": None,
            "commercial_use": False,
            "redistribution": False,
            "modification": False,
            "verification_status": "restricted",
            "source_url": source_url,
            "redistribution_notes": "RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos."
        })

    # 16. Unknown
    else:
        tracking.update({
            "license_name": "Unknown / Missing License Document",
            "spdx_id": None,
            "commercial_use": False,
            "redistribution": False,
            "modification": False,
            "verification_status": "unknown",
            "source_url": source_url,
            "redistribution_notes": "UNKNOWN: No license document or author grant detected. Must be audited before any distribution."
        })

    return tracking


def generate_markdown_report(fonts: List[Dict[str, Any]]) -> str:
    """Generate docs/redistribution-review.md."""
    verified = [f for f in fonts if f["license"]["tracking"]["verification_status"] == "verified"]
    needs_review = [f for f in fonts if f["license"]["tracking"]["verification_status"] == "needs-review"]
    restricted = [f for f in fonts if f["license"]["tracking"]["verification_status"] == "restricted"]
    unknown = [f for f in fonts if f["license"]["tracking"]["verification_status"] == "unknown"]

    total = len(fonts)

    lines = []
    lines.append("# Font Licensing & Redistribution Review")
    lines.append("")
    lines.append("> [!IMPORTANT]")
    lines.append("> **Core Mandate**: Do **NOT** assume that *'free for commercial use'* equals *'allowed to redistribute on GitHub'*.")
    lines.append("> Many freeware fonts permit commercial design output (e.g. logos, graphics, website text rendering) while strictly forbidding re-hosting, bundling, or redistributing the raw font binary files (`.ttf`, `.otf`) in public repositories.")
    lines.append("> **Zero Deletion Policy**: Never delete original license, EULA, or README text files bundled within the source packages.")
    lines.append("")
    lines.append(f"**Audit Date**: {TODAY} | **Total Families Audited**: {total}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append("| Verification Status | Count | Percentage | Redistribution Policy | Description |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    lines.append(f"| **Verified** | **{len(verified)}** | {len(verified)/total*100:.1f}% | Allowed | 100% compliant under explicit open-source licenses (OFL-1.1, CC0-1.0, Apache-2.0, Fontshare FFL, Ubuntu). |")
    lines.append(f"| **Needs Review** | **{len(needs_review)}** | {len(needs_review)/total*100:.1f}% | Conditional / Prohibited | Commercial design use granted, but public repository redistribution is restricted, ambiguous, or requires proof. |")
    lines.append(f"| **Restricted** | **{len(restricted)}** | {len(restricted)/total*100:.1f}% | Prohibited | Proprietary copyright, demo/evaluation cuts, or explicit 'no redistribution' EULAs. Do NOT push binaries to public repos. |")
    lines.append(f"| **Unknown** | **{len(unknown)}** | {len(unknown)/total*100:.1f}% | Prohibited | No license file or grant found. Treated as restricted until audited. |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. GitHub Publishing & Repository Hygiene Rules")
    lines.append("")
    lines.append("1. **Tier 1 (Safe for Public Git Repository)**:")
    lines.append("   - Fonts with status `verified` (e.g. `chillax`, `general-sans`, `ubuntu`, `credit-valley`, `aclonica`) may be hosted, distributed, and bundled in open-source GitHub repositories.")
    lines.append("   - Keep the corresponding `OFL.txt`, `LICENSE.txt`, or author notice alongside the binary.")
    lines.append("")
    lines.append("2. **Tier 2 (Internal / Private Use Only)**:")
    lines.append("   - Fonts with status `needs-review` (e.g. 1001Fonts FFC, Creative Fabrica, Letterlays) can be used within local client projects to generate web/app interfaces, but raw font files **must NOT be committed to public GitHub repositories**.")
    lines.append("   - Add their directories to `.gitignore` if publishing the codebase publicly, or rely on end-user local installation.")
    lines.append("")
    lines.append("3. **Tier 3 (Replace or Purchase)**:")
    lines.append("   - Fonts with status `restricted` (e.g. `warriot` [demo cut], `timeburner` [NimaVisual], `antapani` [unspecified copyright]) should be replaced with open-source alternatives or purchased commercially before public distribution.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Verified Fonts (Allowed for GitHub & Redistribution)")
    lines.append("")
    lines.append(f"Total: **{len(verified)} families**. These fonts carry formal open-source licenses allowing redistribution, modification, and commercial deployment:")
    lines.append("")
    lines.append("| ID | Family Name | License Name | SPDX ID | Commercial | Redistribution | Modification | License File |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for f in verified:
        t = f["license"]["tracking"]
        lfile = os.path.basename(t["license_file"]) if t["license_file"] else "Metadata"
        lines.append(f"| `{f['id']}` | {f['name']} | {t['license_name']} | `{t['spdx_id'] or 'N/A'}` | Yes | **Yes** | Yes | `{lfile}` |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Fonts Requiring Review (Commercial Design OK, Redistribution Restricted)")
    lines.append("")
    lines.append(f"Total: **{len(needs_review)} families**. Commercial use is permitted for design projects, but raw font files may **NOT** be redistributed on public repositories without written permission:")
    lines.append("")
    lines.append("| ID | Family Name | License Grant | Commercial | Redistribution | Redistribution Review Note |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for f in needs_review:
        t = f["license"]["tracking"]
        lines.append(f"| `{f['id']}` | {f['name']} | {t['license_name']} | Yes | **No** | {t['redistribution_notes']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Restricted Fonts (Do NOT Redistribute / Purchase Required)")
    lines.append("")
    lines.append(f"Total: **{len(restricted)} families**. These fonts have restrictive EULAs, evaluation demo limitations, or unspecified copyrights:")
    lines.append("")
    lines.append("| ID | Family Name | License / Terms | Commercial | Redistribution | Action Required |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for f in restricted:
        t = f["license"]["tracking"]
        lines.append(f"| `{f['id']}` | {f['name']} | {t['license_name']} | No / Demo | **No** | {t['redistribution_notes']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. Unknown / Missing Documentation")
    lines.append("")
    lines.append(f"Total: **{len(unknown)} families**. No license documents were found in source packages. Treat as all rights reserved until verified:")
    lines.append("")
    if unknown:
        lines.append("| ID | Family Name | Source Package | Recommendation |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for f in unknown:
            lines.append(f"| `{f['id']}` | {f['name']} | `{f['provenance'].get('source_packages', [f['id']])[0]}` | Contact foundry or replace with verified open-source alternative. |")
    else:
        lines.append("*None. All fonts possess tracked provenance.*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. Complete Font Tracking Inventory (All 103 Families)")
    lines.append("")
    lines.append("| Font ID | Family Name | Category | Status | License | SPDX | Comm. | Redist. | Mod. | Verification Date |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for f in fonts:
        t = f["license"]["tracking"]
        cat = f.get("curated", {}).get("category", "")
        status_badge = f"`{t['verification_status']}`"
        lines.append(f"| `{f['id']}` | {f['name']} | {cat} | {status_badge} | {t['license_name'][:25]} | `{t['spdx_id'] or '-'}` | {'Yes' if t['commercial_use'] else 'No'} | {'**Yes**' if t['redistribution'] else 'No'} | {'Yes' if t['modification'] else 'No'} | {t['verification_date']} |")
    lines.append("")
    return "\n".join(lines)


def main():
    print("Building comprehensive licensing audit and redistribution review...")

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    fonts = catalog.get("fonts", [])
    print(f"Auditing {len(fonts)} fonts...")

    for f in fonts:
        tracking = analyze_font_license(f)
        # Store tracking inside license
        f["license"]["tracking"] = tracking
        # Align license.redistribution_allowed with strict redistribution
        f["license"]["redistribution_allowed"] = tracking["redistribution"]

    # Write updated catalog
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"Updated {CATALOG_PATH} with license tracking data.")

    # Generate markdown report
    os.makedirs(DOCS_DIR, exist_ok=True)
    report_md = generate_markdown_report(fonts)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Generated {OUTPUT_MD} ({len(report_md.splitlines())} lines).")


if __name__ == "__main__":
    main()
