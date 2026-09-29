#!/usr/bin/env python3
"""
normalize_licenses.py - Clean up and finalize licensing terminology in Font Intelligence.

Separates all licensing concepts cleanly:
- commercial_use (bool)
- redistribution_allowed (bool)
- modification_allowed (bool)
- open_source (bool)
- type / license_type (str)
- verification_status (str: verified, needs-review, restricted, unknown)
- labels (list: FREE FOR COMMERCIAL USE, FREE FOR PERSONAL & COMMERCIAL USE, OPEN SOURCE, REDISTRIBUTABLE)
"""

import sys
import os
import json
import re
from typing import Dict, Any, List

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
SKILL_CATALOG_PATH = os.path.join(ROOT_DIR, ".agents", "skills", "font-intelligence", "catalog", "fonts.json")

def clean_encoding(text: str) -> str:
    """Clean legacy encoding artifacts from text strings."""
    if not text:
        return ""
    replacements = {
        "Eimantas Pakonis": "Eimantas Paškonis",
        "Eimantas Pa\ufffdkonis": "Eimantas Paškonis",
        "garute": "Garute",
        "typeface ": "Typeface ©",
        "copyright ": "Copyright ©",
        "": ""
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()

def inspect_font_package_info(font: Dict[str, Any]) -> Dict[str, Any]:
    """Inspect reference files or info.txt directly to detect original author grants."""
    fid = font["id"]
    refs = font.get("license", {}).get("reference_files", [])
    pkgs = font.get("provenance", {}).get("source_packages", [])

    info_data = {}
    for p in pkgs:
        info_path = os.path.join(ROOT_DIR, "All fonts", p, "info.txt")
        if os.path.exists(info_path):
            try:
                content = open(info_path, "r", encoding="utf-8-sig", errors="ignore").read()
                lic_match = re.search(r"license:\s*([^\r\n]+)", content, re.IGNORECASE)
                link_match = re.search(r"link:\s*([^\r\n]+)", content, re.IGNORECASE)
                if lic_match:
                    info_data["info_license"] = lic_match.group(1).strip()
                if link_match:
                    info_data["info_link"] = link_match.group(1).strip()
                if info_path.replace(ROOT_DIR + os.sep, "").replace("\\", "/") not in refs:
                    refs.append(info_path.replace(ROOT_DIR + os.sep, "").replace("\\", "/"))
            except Exception:
                pass
    return info_data

def process_license(font: Dict[str, Any]) -> Dict[str, Any]:
    fid = font["id"]
    lic = font.get("license", {})
    track = lic.get("tracking", {})
    ltype = lic.get("type", "Unknown")
    ref_files = list(lic.get("reference_files", []))
    source_url = track.get("source_url") or lic.get("source_url") or lic.get("license_url")

                                            
    pkg_info = inspect_font_package_info(font)
    info_lic = pkg_info.get("info_license", "")
    info_link = pkg_info.get("info_link", "")
    if info_link and not source_url:
        source_url = info_link

                             
    ltype = clean_encoding(ltype)

                                                                        
    if fid == "umbara":
        ltype = "Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)"
        source_url = "https://creativecommons.org/licenses/by-sa/4.0/"
    elif fid == "neris":
        ltype = "Eimantas Paškonis EULA (Commercial OK, No Redistribution)"
    elif fid == "the-bold-font":
        ltype = "Freeware (Author Freeware Grant)"
        source_url = "https://www.dafont.com/the-bold-font.font"
    elif fid == "garute":
        ltype = "Freeware (Free Commercial - MJType Grant)"
        source_url = "https://mjtype.com"
    elif fid == "zt-shago":
        ltype = "1001Fonts Free Commercial License (FFC)"
        source_url = "https://www.1001fonts.com/zt-shago-font.html"
    elif fid in ["antapani"]:
        ltype = "Evaluation / Demo Cut (Commercial Purchase Required)"
        source_url = "https://www.myfonts.com"
    elif fid in ["bjorn", "lokro"]:
        ltype = "Evaluation / Personal Use Demo"
    elif fid == "bedizen":
        ltype = "Freeware (Tepid Monkey Freeware Grant)"
    elif fid == "enter-sansman":
        ltype = "Freeware (Redistributable Freeware Grant)"
    elif info_lic:
                                                        
        if "sil open font license" in info_lic.lower() or "ofl" in info_lic.lower():
            ltype = "SIL Open Font License 1.1 (OFL)"
        elif "public domain" in info_lic.lower():
            ltype = "Creative Commons Zero 1.0 (CC0) / Public Domain"
        elif "creative commons (by-sa)" in info_lic.lower():
            ltype = "Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)"
        elif "freeware" in info_lic.lower():
            ltype = "Freeware"

    ltype_low = ltype.lower()

                                              
                                                                    
    is_open_source = any(k in ltype_low for k in [
        "sil open font license", "ofl", "apache license 2.0", "apache-2.0",
        "creative commons zero", "cc0", "public domain dedication",
        "creative commons attribution-sharealike 4.0", "cc by-sa 4.0"
    ])

                                       
                                                                             
    is_modification_allowed = is_open_source or (fid in ["bm-dohyeon", "tao-baso", "waloh"])
    if "modification" in track and not is_open_source:
        is_modification_allowed = bool(track["modification"])

                                         
                                                               
    is_redist = False
    if is_open_source:
        is_redist = True
    elif "fontshare" in ltype_low or "itf free font license" in ltype_low:
        is_redist = True
    elif fid in ["enter-sansman", "bedizen"]:
        is_redist = True

                                 
    comm_use = False
    if is_open_source or "fontshare" in ltype_low:
        comm_use = True
    elif any(k in ltype_low for k in [
        "free commercial", "commercial use allowed", "commercial use for everyone",
        "personal & commercial", "personal and commercial", "receipt pdf",
        "author grant", "commercial ok", "befonts grant", "khurasan", "mjtype grant",
        "tepid monkey freeware grant", "redistributable freeware grant"
    ]):
        comm_use = True
    elif "1001fonts free commercial" in ltype_low:
        comm_use = True
    elif "creative fabrica" in ltype_low:
        comm_use = True
    elif info_lic.lower() == "freeware":
                                                                                                         
        comm_use = True

                                              
    if any(k in ltype_low for k in ["personal use only", "personal use demo", "evaluation / demo cut", "purchase required"]):
        comm_use = False

                                      
    if is_open_source:
        vstat = "verified"
    elif "fontshare" in ltype_low or fid in ["chillax", "general-sans"]:
        vstat = "verified"
    elif "unknown" in ltype_low:
        vstat = "unknown"
    elif any(k in ltype_low for k in ["personal use only", "personal use demo", "evaluation / demo cut", "purchase required"]):
        vstat = "restricted"
    elif comm_use and (ref_files or source_url):
        vstat = "verified"
    elif not comm_use:
        vstat = "restricted"
    else:
        vstat = "needs-review"

                             
    if is_open_source or (is_redist and comm_use):
        risk_level = "permissive"
    elif "commercial_proof_needed" in lic.get("risk_level", "") or "creative fabrica" in ltype_low or "letterlays" in ltype_low:
        risk_level = "commercial_proof_needed"
    elif "freeware" in ltype_low:
        risk_level = "freeware"
    elif vstat == "unknown" or "unknown" in ltype_low:
        risk_level = "unknown"
    elif vstat == "restricted" or not comm_use:
        risk_level = "restricted"
    else:
        risk_level = "unknown"

                                                
    labels = []
    if is_open_source:
        labels.append("OPEN SOURCE")

    has_personal_and_commercial = False
    if is_open_source or "fontshare" in ltype_low:
        has_personal_and_commercial = True
    elif any(k in ltype_low for k in [
        "personal & commercial", "personal and commercial", "for everyone",
        "anything you want", "100% free", "free for personal use & commercial use",
        "tepid monkey", "redistributable freeware", "author freeware grant"
    ]) or info_lic.lower() == "freeware":
        has_personal_and_commercial = True

    if comm_use:
        if has_personal_and_commercial:
            labels.append("FREE FOR PERSONAL & COMMERCIAL USE")
        else:
            labels.append("FREE FOR COMMERCIAL USE")
    else:
        if any(k in ltype_low for k in ["personal", "demo"]):
            labels.append("PERSONAL USE ONLY")
        else:
            labels.append("NEEDS REVIEW")

    if is_redist:
        labels.append("REDISTRIBUTABLE")

                            
    updated_tracking = dict(track) if track else {}
    updated_tracking["license_name"] = ltype
    updated_tracking["commercial_use"] = comm_use
    updated_tracking["redistribution"] = is_redist
    updated_tracking["modification"] = is_modification_allowed
    updated_tracking["open_source"] = is_open_source
    updated_tracking["verification_status"] = vstat
    updated_tracking["verification_date"] = "2026-09-29"
    if source_url:
        updated_tracking["source_url"] = source_url

    return {
        "type": ltype,
        "license_type": ltype,
        "commercial_use": comm_use,
        "redistribution_allowed": is_redist,
        "modification_allowed": is_modification_allowed,
        "open_source": is_open_source,
        "verification_status": vstat,
        "labels": labels,
        "risk_level": risk_level,
        "reference_files": ref_files,
        "license_url": lic.get("license_url"),
        "source_url": source_url,
        "verification_date": "2026-09-29",
        "tracking": updated_tracking
    }

def main():
    print("=" * 80)
    print("FONT INTELLIGENCE: NORMALIZING & FINALIZING LICENSING TERMINOLOGY")
    print("=" * 80)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    fonts = catalog.get("fonts", [])
    print(f"Processing {len(fonts)} families...")

    open_source_count = 0
    comm_use_count = 0
    redist_count = 0
    freeware_count = 0

    for f in fonts:
        new_lic = process_license(f)
        f["license"] = new_lic

                                                                                      
        if new_lic["redistribution_allowed"]:
            f["distribution_status"] = "public-asset"
        elif new_lic["verification_status"] == "restricted" or not new_lic["commercial_use"]:
            f["distribution_status"] = "restricted"
        else:
            f["distribution_status"] = "catalog-only"

        if new_lic["open_source"]:
            open_source_count += 1
        if new_lic["commercial_use"]:
            comm_use_count += 1
        if new_lic["redistribution_allowed"]:
            redist_count += 1
        if "freeware" in new_lic["type"].lower():
            freeware_count += 1

    print(f"• Total Families:               {len(fonts)}")
    print(f"• Open Source Confirmed:        {open_source_count}")
    print(f"• Commercial Use Confirmed:     {comm_use_count}")
    print(f"• Publicly Redistributable:     {redist_count}")
    print(f"• Freeware (Non-Open-Source):   {freeware_count}")

                        
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"[OK] Updated {CATALOG_PATH}")

                         
    if os.path.exists(os.path.dirname(SKILL_CATALOG_PATH)):
        with open(SKILL_CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"[OK] Updated {SKILL_CATALOG_PATH}")

    print("=" * 80)
    print("NORMALIZATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
