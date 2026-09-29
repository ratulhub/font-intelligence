#!/usr/bin/env python3
"""
scan_fonts.py - Scan font packages, detect font files, and extract OpenType metadata.

Scans directories or individual font files (.ttf, .otf, .woff, .woff2),
extracts family names, weights, scripts, unicode blocks, variable font axes,
and OS/2.fsType embedding permissions using fontTools.
"""

import os
import sys
import json
import argparse
import hashlib
from typing import Dict, List, Any, Optional

try:
    from fontTools.ttLib import TTFont
except ImportError:
    TTFont = None

sys.stdout.reconfigure(encoding='utf-8')

                                    
UNICODE_BLOCK_SCRIPTS = {
    "Basic Latin": "Latin",
    "Latin-1 Supplement": "Latin",
    "Latin Extended-A": "Latin",
    "Latin Extended-B": "Latin",
    "Cyrillic": "Cyrillic",
    "Cyrillic Supplement": "Cyrillic",
    "Greek and Coptic": "Greek",
    "Greek Extended": "Greek",
    "Devanagari": "Devanagari",
    "Bengali": "Bangla",
    "Arabic": "Arabic",
    "Hangul Syllables": "Hangul",
    "Hangul Jamo": "Hangul",
    "CJK Unified Ideographs": "CJK",
    "Hiragana": "Japanese",
    "Katakana": "Japanese",
}

FS_TYPE_DESCRIPTIONS = {
    0x0000: "Installable Embedding (Fully Permissive)",
    0x0002: "Restricted License Embedding (Cannot be embedded)",
    0x0004: "Preview & Print Embedding",
    0x0008: "Editable Embedding (Permissive)",
}

def compute_sha256(filepath: str) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def decode_name_record(record) -> str:
    """Decode an OpenType name record string safely."""
    try:
        return record.toUnicode()
    except Exception:
        try:
            return record.string.decode("utf-16-be", errors="ignore")
        except Exception:
            return str(record.string)

def extract_font_metadata(file_path: str) -> Dict[str, Any]:
    """Extract metadata from a single font binary using fontTools."""
    meta = {
        "file_name": os.path.basename(file_path),
        "file_path": file_path.replace("\\", "/"),
        "file_size_bytes": os.path.getsize(file_path),
        "file_format": os.path.splitext(file_path)[1].lower().lstrip("."),
        "sha256": compute_sha256(file_path),
        "family_name": "",
        "subfamily_name": "Regular",
        "postscript_name": "",
        "version": "",
        "weight": 400,
        "width_class": 5,
        "italic": False,
        "is_variable": False,
        "variable_axes": [],
        "fs_type": 0,
        "embedding_permission": "Installable Embedding",
        "scripts": ["Latin"],
        "unicode_blocks": [],
        "glyph_count": 0,
    }

    if not TTFont:
        return meta

    try:
        tt = TTFont(file_path, fontNumber=0, lazy=True)

                               
        if "name" in tt:
            for rec in tt["name"].names:
                nid = rec.nameID
                val = decode_name_record(rec).strip()
                if not val:
                    continue
                if nid == 1 and not meta["family_name"]:
                    meta["family_name"] = val
                elif nid == 2 and meta["subfamily_name"] == "Regular":
                    meta["subfamily_name"] = val
                elif nid == 4 and not meta.get("full_name"):
                    meta["full_name"] = val
                elif nid == 5 and not meta["version"]:
                    meta["version"] = val
                elif nid == 6 and not meta["postscript_name"]:
                    meta["postscript_name"] = val
                elif nid == 16:                      
                    meta["family_name"] = val
                elif nid == 17:                         
                    meta["subfamily_name"] = val

                               
        if "OS/2" in tt:
            os2 = tt["OS/2"]
            meta["weight"] = int(getattr(os2, "usWeightClass", 400))
            meta["width_class"] = int(getattr(os2, "usWidthClass", 5))
            meta["fs_type"] = int(getattr(os2, "fsType", 0))

                           
            fs_val = meta["fs_type"]
            if fs_val == 0:
                meta["embedding_permission"] = "Installable Embedding (Permissive)"
            elif fs_val & 0x0002:
                meta["embedding_permission"] = "Restricted License Embedding"
            elif fs_val & 0x0004:
                meta["embedding_permission"] = "Preview & Print Embedding"
            elif fs_val & 0x0008:
                meta["embedding_permission"] = "Editable Embedding (Permissive)"
            else:
                meta["embedding_permission"] = f"Other (fsType={fs_val})"

                          
            fs_selection = getattr(os2, "fsSelection", 0)
            if fs_selection & 0x01:
                meta["italic"] = True

                             
        if "fvar" in tt:
            meta["is_variable"] = True
            for axis in tt["fvar"].axes:
                meta["variable_axes"].append({
                    "tag": axis.axisTag,
                    "min_value": axis.minValue,
                    "default_value": axis.defaultValue,
                    "max_value": axis.maxValue,
                })

                                      
        if "maxp" in tt:
            meta["glyph_count"] = int(getattr(tt["maxp"], "numGlyphs", 0))

        detected_scripts = set(["Latin"])
        detected_blocks = set()

        if "cmap" in tt:
            cmap = tt.getBestCmap()
            if cmap:
                for cp in cmap.keys():
                    if 0x0400 <= cp <= 0x04FF or 0x0500 <= cp <= 0x052F:
                        detected_scripts.add("Cyrillic")
                        detected_blocks.add("Cyrillic")
                    elif 0x0370 <= cp <= 0x03FF or 0x1F00 <= cp <= 0x1FFF:
                        detected_scripts.add("Greek")
                        detected_blocks.add("Greek")
                    elif 0x0900 <= cp <= 0x097F:
                        detected_scripts.add("Devanagari")
                        detected_blocks.add("Devanagari")
                    elif 0x0980 <= cp <= 0x09FF:
                        detected_scripts.add("Bangla")
                        detected_blocks.add("Bengali")
                    elif 0x0600 <= cp <= 0x06FF:
                        detected_scripts.add("Arabic")
                        detected_blocks.add("Arabic")
                    elif 0xAC00 <= cp <= 0xD7AF or 0x1100 <= cp <= 0x11FF:
                        detected_scripts.add("Hangul")
                        detected_blocks.add("Hangul")
                    elif 0x4E00 <= cp <= 0x9FFF:
                        detected_scripts.add("CJK")
                        detected_blocks.add("CJK Unified Ideographs")

        meta["scripts"] = sorted(list(detected_scripts))
        meta["unicode_blocks"] = sorted(list(detected_blocks))

        tt.close()
    except Exception as e:
        meta["scan_error"] = str(e)

    if not meta["family_name"]:
        meta["family_name"] = os.path.splitext(os.path.basename(file_path))[0]

    return meta

def scan_source(source_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Scan a directory or file and extract metadata for all font binaries."""
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source path does not exist: {source_path}")

    font_files = []
    valid_exts = {".ttf", ".otf", ".woff", ".woff2"}

    if os.path.isfile(source_path):
        ext = os.path.splitext(source_path)[1].lower()
        if ext in valid_exts:
            font_files.append(os.path.abspath(source_path))
    else:
        for root, _, files in os.walk(source_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in valid_exts:
                    font_files.append(os.path.abspath(os.path.join(root, file)))

    font_files.sort()
    if limit and limit > 0:
        font_files = font_files[:limit]

    results = []
    for fp in font_files:
        results.append(extract_font_metadata(fp))
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Scan font packages, detect font files, and extract OpenType metadata."
    )
    parser.add_argument(
        "--source",
        default="All fonts",
        help="Path to directory or single font file to scan (default: 'All fonts')",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write JSON output",
    )
    parser.add_argument(
        "--format",
        choices=["summary", "json", "compact"],
        default="summary",
        help="Output format (summary, json, compact). Default: summary",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of font files scanned",
    )

    args = parser.parse_args()

                                            
    source_path = os.path.abspath(args.source)
    if not os.path.exists(source_path):
                                        
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        alt_path = os.path.join(root_dir, args.source)
        if os.path.exists(alt_path):
            source_path = alt_path
        else:
            print(f"Error: Source path '{args.source}' does not exist.", file=sys.stderr)
            sys.exit(1)

    print(f"Scanning font source: {source_path} ...", file=sys.stderr)
    try:
        results = scan_source(source_path, limit=args.limit)
    except Exception as e:
        print(f"Scan error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out_dir = os.path.dirname(os.path.abspath(args.output))
        os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Saved {len(results)} scanned font records to: {args.output}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    elif args.format == "compact":
        for r in results:
            var_str = f" [VAR: {len(r['variable_axes'])} axes]" if r["is_variable"] else ""
            print(f"{r['family_name']} | {r['subfamily_name']} | W{r['weight']} | {r['file_format'].upper()}{var_str} | Scripts: {', '.join(r['scripts'])} | {r['file_name']}")
    else:
                      
        families = set(r["family_name"] for r in results)
        formats = {}
        for r in results:
            fmt = r["file_format"]
            formats[fmt] = formats.get(fmt, 0) + 1

        print("=" * 80)
        print("FONT SCAN & METADATA EXTRACTION REPORT")
        print("=" * 80)
        print(f"• Total Font Binaries Detected: {len(results)}")
        print(f"• Unique Families Identified:   {len(families)}")
        print(f"• Formats Breakdown:            {', '.join(f'{k.upper()}: {v}' for k, v in sorted(formats.items()))}")
        print("-" * 80)
        print(f"FIRST 10 FONT BINARIES:")
        for idx, r in enumerate(results[:10], 1):
            var_badge = " [VARIABLE]" if r["is_variable"] else ""
            print(f"[{idx}] {r['family_name']} ({r['subfamily_name']}) - {r['file_format'].upper()}{var_badge}")
            print(f"    Weight: {r['weight']} | Glyphs: {r['glyph_count']} | Embedding: {r['embedding_permission']}")
            print(f"    Scripts: {', '.join(r['scripts'])}")
            print(f"    File: {r['file_name']} ({r['file_size_bytes'] / 1024:.1f} KB)")
        if len(results) > 10:
            print(f"\n... and {len(results) - 10} more font binaries.")
        print("=" * 80)

if __name__ == "__main__":
    main()
