import os
import sys
import json
import re
import hashlib
from datetime import datetime, timezone
from collections import defaultdict
import fontTools.ttLib
import jsonschema

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"D:\font-intelligence"
FONTS_DIR = os.path.join(ROOT_DIR, "All fonts")
TARGET_DIRS = [
    os.path.join(ROOT_DIR, "catalog")
]

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "FontIntelligenceCatalog",
    "description": "Canonical Font Intelligence Catalog Schema separating verified technical font metadata from curated design intelligence.",
    "type": "object",
    "required": ["$schema", "version", "generated_at", "generator", "total_families", "fonts"],
    "properties": {
        "$schema": {"type": "string"},
        "version": {"type": "string"},
        "generated_at": {"type": "string"},
        "generator": {"type": "string"},
        "total_families": {"type": "integer", "minimum": 1},
        "fonts": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "id",
                    "name",
                    "aliases",
                    "curated",
                    "technical",
                    "files",
                    "provenance",
                    "license"
                ],
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
                    },
                    "name": {"type": "string"},
                    "aliases": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "curated": {
                        "type": "object",
                        "description": "CURATED design information (can be customized/edited and will be preserved across regenerations).",
                        "required": ["category", "subtype", "styles", "roles", "readability", "fallback"],
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["sans-serif", "serif", "display", "handwriting", "monospace"]
                            },
                            "subtype": {"type": "string"},
                            "styles": {
                                "type": "array",
                                "minItems": 1,
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "modern", "premium", "luxury", "editorial", "fashion", "technical",
                                        "corporate", "playful", "classic", "futuristic", "minimal", "brutalist",
                                        "industrial", "geometric", "humanist", "retro", "vintage", "organic",
                                        "grunge", "art-deco", "decorative", "handwritten"
                                    ]
                                }
                            },
                            "roles": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": ["display", "hero", "heading", "body", "ui", "UI", "button", "number", "caption", "code", "logo", "branding", "accent"]
                                }
                            },
                            "readability": {
                                "type": "object",
                                "required": ["body", "long_form", "ui", "small_text", "numbers"],
                                "properties": {
                                    "body": {"type": "integer", "minimum": 1, "maximum": 10},
                                    "long_form": {"type": "integer", "minimum": 1, "maximum": 10},
                                    "ui": {"type": "integer", "minimum": 1, "maximum": 10},
                                    "small_text": {"type": "integer", "minimum": 1, "maximum": 10},
                                    "numbers": {"type": "integer", "minimum": 1, "maximum": 10},
                                    "factors": {"type": "object"}
                                }
                            },
                            "fallback": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "notes": {"type": ["string", "null"]}
                        }
                    },
                    "technical": {
                        "type": "object",
                        "description": "VERIFIED technical data extracted directly from font binary tables.",
                        "required": [
                            "weights",
                            "italic",
                            "variable",
                            "axes",
                            "scripts",
                            "languages",
                            "unicode_blocks",
                            "total_glyphs",
                            "opentype_features",
                            "embedding_permission"
                        ],
                        "properties": {
                            "weights": {
                                "type": "array",
                                "items": {"type": "integer"}
                            },
                            "italic": {"type": "boolean"},
                            "variable": {"type": "boolean"},
                            "axes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["tag", "name", "min", "default", "max"],
                                    "properties": {
                                        "tag": {"type": "string"},
                                        "name": {"type": "string"},
                                        "min": {"type": "number"},
                                        "default": {"type": "number"},
                                        "max": {"type": "number"}
                                    }
                                }
                            },
                            "scripts": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "languages": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "unicode_blocks": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "total_glyphs": {"type": "integer"},
                            "opentype_features": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "embedding_permission": {"type": "string"}
                        }
                    },
                    "files": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["path", "format", "weight", "style", "variable", "size_bytes", "sha256"],
                            "properties": {
                                "path": {"type": "string"},
                                "format": {
                                    "type": "string",
                                    "enum": ["otf", "ttf", "woff", "woff2", "eot"]
                                },
                                "weight": {"type": ["integer", "null"]},
                                "style": {
                                    "type": "string",
                                    "enum": ["normal", "italic"]
                                },
                                "variable": {"type": "boolean"},
                                "size_bytes": {"type": "integer"},
                                "sha256": {"type": "string"}
                            }
                        }
                    },
                    "provenance": {
                        "type": "object",
                        "required": ["source_packages", "designer", "manufacturer", "version", "copyright"],
                        "properties": {
                            "source_packages": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "designer": {"type": ["string", "null"]},
                            "manufacturer": {"type": ["string", "null"]},
                            "designer_url": {"type": ["string", "null"]},
                            "vendor_url": {"type": ["string", "null"]},
                            "version": {"type": ["string", "null"]},
                            "copyright": {"type": ["string", "null"]}
                        }
                    },
                    "license": {
                        "type": "object",
                        "required": ["type", "commercial_use", "redistribution_allowed", "risk_level", "reference_files"],
                        "properties": {
                            "type": {"type": "string"},
                            "commercial_use": {"type": "boolean"},
                            "redistribution_allowed": {"type": "boolean"},
                            "risk_level": {
                                "type": "string",
                                "enum": ["permissive", "freeware", "commercial_proof_needed", "restricted", "unknown"]
                            },
                            "reference_files": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "license_url": {"type": ["string", "null"]}
                        }
                    }
                }
            }
        }
    }
}

def get_file_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def normalize_font_id(name):
    clean = re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()
    return clean

def get_name_record(names, name_id):
    records = [r for r in names if r.nameID == name_id]
    if not records:
        return None
    for r in records:
        if r.platformID == 3 and r.langID == 0x409:
            try: return r.toUnicode()
            except Exception: pass
    for r in records:
        if r.platformID == 1 and r.langID == 0:
            try: return r.toUnicode()
            except Exception: pass
    for r in records:
        try: return r.toUnicode()
        except Exception: pass
    return None

def resolve_canonical_family_name(fam_raw, pkg_name, fn):
    fam = (fam_raw or '').strip()
    pkg_low = pkg_name.lower()
    fn_low = fn.lower()
    
    if 'chillax' in pkg_low: return 'Chillax'
    if 'generalsans' in pkg_low or 'general sans' in fam.lower(): return 'General Sans'
    if 'heming' in pkg_low: return 'Heming'
    if 'dohyeon' in pkg_low: return 'BM DoHyeon'
    if 'garute' in pkg_low: return 'Garute'
    if 'cuyabra' in pkg_low: return 'Cuyabra'
    if 'timeburner' in pkg_low: return 'Timeburner'
    if 'warriot' in pkg_low: return 'Warriot'
    if 'zillah' in pkg_low: return 'Zillah Modern'
    if 'credit' in pkg_low:
        if 'river' in fam.lower() or 'river' in fn_low: return 'Credit River'
        if 'valley' in fam.lower() or 'valley' in fn_low: return 'Credit Valley'
    if 'reckoner' in pkg_low: return 'Reckoner'
    if 'ubuntu' == pkg_low:
        if 'mono' in fam.lower() or 'mono' in fn_low: return 'Ubuntu Mono'
        if 'condensed' in fam.lower() or 'condensed' in fn_low: return 'Ubuntu Condensed'
        return 'Ubuntu'
    if pkg_name == 'behance-6596a9ca1f6c5': return 'Al Saflers'
    if pkg_name == 'behance-65c4bcf7464f1': return 'Biocats'
    if pkg_name == 'behance-65ef07bdb6f6f': return 'Pingsan'
    if pkg_name == 'behance-672092c703c71': return 'Halo Dek'
    if pkg_name == 'behance-68ff9b50e17d5': return 'Spicy Sale'
    if pkg_name == 'behance-6a4cfe40dec36': return 'Butflow'
    if 'the-bold-font' in pkg_low: return 'THE BOLD FONT'
    if 'new-shape' == pkg_low: return 'NewShape'
    if 'newest-shape' == pkg_low: return 'NewestShape'
    if 'aix-milan' == pkg_low: return 'Aix Milan'
    if 'jazzy-huitbits' == pkg_low: return 'Jazzy HuitBits'
    
    if fam.endswith(' Variable'): fam = fam[:-9].strip()
    if fam.endswith(' Oblique') and len(fam) > 8: fam = fam[:-8].strip()
    if fam.endswith(' OTF') and len(fam) > 4: fam = fam[:-4].strip()
    if fam.endswith(' TTF') and len(fam) > 4: fam = fam[:-4].strip()
    
    if not fam or fam.lower() in ['unnamed', 'unknown']:
        fam = pkg_name.replace('-', ' ').title()
    return fam

def extract_features_and_scripts(font):
    features = set()
    scripts = set()
    for tag in ['GSUB', 'GPOS']:
        if tag in font:
            table = font[tag].table
            if hasattr(table, 'FeatureList') and table.FeatureList:
                for fr in table.FeatureList.FeatureRecord:
                    features.add(fr.FeatureTag)
            if hasattr(table, 'ScriptList') and table.ScriptList:
                for sr in table.ScriptList.ScriptRecord:
                    scripts.add(sr.ScriptTag)
    if 'kern' in font:
        features.add('kern')
    return sorted(list(features)), sorted(list(scripts))

def extract_unicode_info(font):
    try:
        cmap = font.getBestCmap()
    except Exception:
        cmap = None
    if not cmap:
        return 0, [], [], []
    codepoints = set(cmap.keys())
    
    block_defs = [
        ("Basic Latin", 0x0020, 0x007E, "Latin"),
        ("Latin-1 Supplement", 0x00A0, 0x00FF, "Latin"),
        ("Latin Extended-A", 0x0100, 0x017F, "Latin"),
        ("Latin Extended-B", 0x0180, 0x024F, "Latin"),
        ("Greek and Coptic", 0x0370, 0x03FF, "Greek"),
        ("Cyrillic", 0x0400, 0x04FF, "Cyrillic"),
        ("Arabic", 0x0600, 0x06FF, "Arabic"),
        ("Devanagari", 0x0900, 0x097F, "Devanagari"),
        ("General Punctuation", 0x2000, 0x206F, None),
        ("Currency Symbols", 0x20A0, 0x20CF, None),
        ("Hiragana", 0x3040, 0x309F, "Japanese"),
        ("Katakana", 0x30A0, 0x30FF, "Japanese"),
        ("Hangul Syllables", 0xAC00, 0xD7AF, "Korean"),
        ("CJK Unified Ideographs", 0x4E00, 0x9FFF, "Chinese/Japanese/Korean"),
    ]
    
    blocks = []
    scripts = set()
    for name, start, end, script in block_defs:
        count = sum(1 for cp in codepoints if start <= cp <= end)
        if count > 0:
            blocks.append(name)
            if script:
                scripts.add(script)
                
    languages = set()
    if any(0x0041 <= cp <= 0x005A for cp in codepoints): languages.add("en")
    if all(cp in codepoints for cp in [ord('é'), ord('à'), ord('è'), ord('ù')]): languages.add("fr")
    if all(cp in codepoints for cp in [ord('ä'), ord('ö'), ord('ü'), ord('ß')]): languages.add("de")
    if all(cp in codepoints for cp in [ord('ñ'), ord('á'), ord('í'), ord('ó'), ord('ú')]): languages.add("es")
    if all(cp in codepoints for cp in [ord('ã'), ord('õ'), ord('ç')]): languages.add("pt")
    if all(cp in codepoints for cp in [ord('à'), ord('è'), ord('é'), ord('ì'), ord('ò'), ord('ù')]): languages.add("it")
    if any(cp in codepoints for cp in [0x0104, 0x0106, 0x0118, 0x0141, 0x0143, 0x015A, 0x0179, 0x017B]): languages.add("pl")
    if any(cp in codepoints for cp in [0x010C, 0x010E, 0x011A, 0x0158, 0x0160, 0x0164, 0x016E, 0x017D]): languages.add("cs")
    if any(0x0410 <= cp <= 0x044F for cp in codepoints): languages.add("ru")
    if any(0xAC00 <= cp <= 0xD7AF for cp in codepoints): languages.add("ko")
    
    if not scripts and codepoints:
        scripts.add("Latin")
    if not languages and codepoints:
        languages.add("en")
        
    return len(codepoints), blocks, sorted(list(scripts)), sorted(list(languages))

def format_fs_type(fst):
    if fst is None or fst == 0:
        return "Installable Embedding (unrestricted)"
    parts = []
    if fst & 0x0002: parts.append("Restricted License")
    if fst & 0x0004: parts.append("Preview & Print Only")
    if fst & 0x0008: parts.append("Editable Embedding")
    if fst & 0x0100: parts.append("No Subsetting")
    return ", ".join(parts) or f"0x{fst:04x}"

FALLBACK_SANS = ["system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "Helvetica Neue", "Arial", "sans-serif"]
FALLBACK_SERIF = ["Georgia", "Cambria", "Times New Roman", "Times", "serif"]
FALLBACK_MONO = ["ui-monospace", "Cascadia Code", "Source Code Pro", "Menlo", "Consolas", "monospace"]
FALLBACK_DISPLAY = ["Impact", "Arial Black", "Trebuchet MS", "sans-serif"]
FALLBACK_HANDWRITING = ["Comic Sans MS", "Chalkboard", "Segoe Script", "cursive"]

DESIGN_DEFAULTS = {
    "General Sans": {"category": "sans-serif", "subtype": "geometric-neo-grotesque", "roles": ["display", "heading", "body", "ui"], "fallback": FALLBACK_SANS},
    "Chillax": {"category": "sans-serif", "subtype": "geometric-contemporary", "roles": ["display", "heading", "ui"], "fallback": FALLBACK_SANS},
    "Ubuntu": {"category": "sans-serif", "subtype": "humanist", "roles": ["body", "ui", "heading"], "fallback": FALLBACK_SANS},
    "Ubuntu Condensed": {"category": "sans-serif", "subtype": "humanist-condensed", "roles": ["display", "heading", "ui"], "fallback": FALLBACK_SANS},
    "Ubuntu Mono": {"category": "monospace", "subtype": "humanist-monospace", "roles": ["code", "ui", "body"], "fallback": FALLBACK_MONO},
    "Dosis": {"category": "sans-serif", "subtype": "rounded-geometric", "roles": ["display", "heading", "ui"], "fallback": FALLBACK_SANS},
    "Aclonica": {"category": "sans-serif", "subtype": "deco-rounded", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Gudea": {"category": "sans-serif", "subtype": "humanist", "roles": ["body", "ui", "heading"], "fallback": FALLBACK_SANS},
    "Simply Sans": {"category": "sans-serif", "subtype": "geometric", "roles": ["body", "heading", "ui"], "fallback": FALLBACK_SANS},
    "Neris": {"category": "sans-serif", "subtype": "geometric-neo-grotesque", "roles": ["display", "heading", "body"], "fallback": FALLBACK_SANS},
    "NewShape": {"category": "sans-serif", "subtype": "modern-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "NewestShape": {"category": "sans-serif", "subtype": "modern-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Viga": {"category": "sans-serif", "subtype": "display-sans", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Courbe Sans": {"category": "sans-serif", "subtype": "high-contrast-sans", "roles": ["display", "heading", "branding"], "fallback": FALLBACK_SANS},
    "Kingsbridge": {"category": "sans-serif", "subtype": "grotesque-condensed-expanded", "roles": ["display", "heading", "ui"], "fallback": FALLBACK_SANS},
    "Oligopoly": {"category": "sans-serif", "subtype": "geometric-modern", "roles": ["display", "heading", "branding"], "fallback": FALLBACK_SANS},
    "Modestic Sans": {"category": "sans-serif", "subtype": "clean-neo-grotesque", "roles": ["display", "heading", "body"], "fallback": FALLBACK_SANS},
    "Reckoner": {"category": "sans-serif", "subtype": "industrial-condensed", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Lokro": {"category": "sans-serif", "subtype": "minimalist-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Timeburner": {"category": "sans-serif", "subtype": "techno-rounded", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Balhattan": {"category": "sans-serif", "subtype": "condensed-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Ithaca": {"category": "serif", "subtype": "high-contrast-display-serif", "roles": ["display", "heading", "accent"], "fallback": FALLBACK_SERIF},
    "Credit Valley": {"category": "serif", "subtype": "transitional-serif", "roles": ["heading", "body"], "fallback": FALLBACK_SERIF},
    "Credit River": {"category": "sans-serif", "subtype": "clean-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "BM DoHyeon": {"category": "sans-serif", "subtype": "hangul-retro-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Bakula": {"category": "handwriting", "subtype": "brush-handwritten", "roles": ["display", "accent", "branding"], "fallback": FALLBACK_HANDWRITING},
    "Anak Bijak": {"category": "handwriting", "subtype": "playful-kids-script", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Anak Gedong": {"category": "handwriting", "subtype": "playful-marker", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Alphakind": {"category": "handwriting", "subtype": "friendly-casual-hand", "roles": ["display", "heading", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Biocats": {"category": "handwriting", "subtype": "casual-organic-script", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Pingsan": {"category": "handwriting", "subtype": "quirky-doodle", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Halo Dek": {"category": "handwriting", "subtype": "friendly-marker", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Spicy Sale": {"category": "handwriting", "subtype": "bold-promo-script", "roles": ["display", "accent", "branding"], "fallback": FALLBACK_HANDWRITING},
    "Butflow": {"category": "handwriting", "subtype": "flowing-script", "roles": ["display", "accent", "branding"], "fallback": FALLBACK_HANDWRITING},
    "Jumping Chick": {"category": "handwriting", "subtype": "cute-cartoon", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Super Joyful": {"category": "handwriting", "subtype": "childish-comic", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Super Malibu": {"category": "handwriting", "subtype": "retro-beach-hand", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Super Starfish": {"category": "handwriting", "subtype": "bubbly-casual", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Sweet School": {"category": "handwriting", "subtype": "cute-chalk-hand", "roles": ["display", "accent"], "fallback": FALLBACK_HANDWRITING},
    "Bjorn": {"category": "display", "subtype": "nordic-uppercase", "roles": ["display", "heading", "branding"], "fallback": FALLBACK_DISPLAY},
    "Castle Chunk": {"category": "display", "subtype": "heavy-slab-chunky", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Delta Block": {"category": "display", "subtype": "heavy-block-futuristic", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Die Nasty": {"category": "display", "subtype": "grunge-distressed", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Free Cheese": {"category": "display", "subtype": "novelty-comic", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Guanine": {"category": "display", "subtype": "sci-fi-techno", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Inflammable Age": {"category": "display", "subtype": "industrial-stencil", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Jazzy HuitBits": {"category": "monospace", "subtype": "pixel-8bit", "roles": ["display", "code", "accent"], "fallback": FALLBACK_MONO},
    "JazzyRabbit": {"category": "display", "subtype": "propaganda-deco", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Neuropol": {"category": "display", "subtype": "futuristic-geom", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Opsilon": {"category": "display", "subtype": "modern-geometric-display", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Paint Marker": {"category": "display", "subtype": "paint-graffiti", "roles": ["display", "accent", "branding"], "fallback": FALLBACK_DISPLAY},
    "Raster Forge": {"category": "monospace", "subtype": "pixel-bitmap", "roles": ["display", "code", "accent"], "fallback": FALLBACK_MONO},
    "Relish Gargler": {"category": "display", "subtype": "heavy-psychedelic", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Ruthless Sketch": {"category": "display", "subtype": "crosshatch-sketch", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Stampcraft": {"category": "display", "subtype": "rubber-stamp", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Street Cred": {"category": "display", "subtype": "urban-graffiti", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Unispace": {"category": "monospace", "subtype": "futuristic-monospace", "roles": ["display", "code", "ui"], "fallback": FALLBACK_MONO},
    "Unsteady Oversteer": {"category": "display", "subtype": "racing-italic-techno", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Vaticanus": {"category": "display", "subtype": "monumental-blackletter", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Wide Road": {"category": "display", "subtype": "ultra-extended-highway", "roles": ["display", "heading", "branding"], "fallback": FALLBACK_DISPLAY},
    "World of Water": {"category": "display", "subtype": "liquid-decorative", "roles": ["display", "accent"], "fallback": FALLBACK_DISPLAY},
    "Zero Cool": {"category": "display", "subtype": "cyberpunk-techno", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Zorque": {"category": "display", "subtype": "chunky-arcade", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "THE BOLD FONT": {"category": "display", "subtype": "impact-all-caps", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "ZT Nature": {"category": "display", "subtype": "botanical-organic", "roles": ["display", "heading", "accent"], "fallback": FALLBACK_DISPLAY},
    "Zt Shago": {"category": "display", "subtype": "heavy-neo-grotesque", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Society": {"category": "display", "subtype": "stencil-modern", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "TALERO": {"category": "display", "subtype": "futuristic-sans", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Warriot": {"category": "display", "subtype": "condensed-esports", "roles": ["display", "heading"], "fallback": FALLBACK_DISPLAY},
    "Garute": {"category": "sans-serif", "subtype": "geometric-grotesque", "roles": ["display", "heading", "body"], "fallback": FALLBACK_SANS},
    "Cuyabra": {"category": "sans-serif", "subtype": "humanist-sans", "roles": ["display", "heading"], "fallback": FALLBACK_SANS},
    "Heming": {"category": "sans-serif", "subtype": "minimalist-contemporary", "roles": ["display", "heading", "body"], "fallback": FALLBACK_SANS},
    "Al Saflers": {"category": "display", "subtype": "stylish-modern-display", "roles": ["display", "heading", "branding"], "fallback": FALLBACK_DISPLAY},
}

def get_curated_info(family_name, existing_curated=None):
    if existing_curated and 'category' in existing_curated and 'roles' in existing_curated:
        return existing_curated
    for k, v in DESIGN_DEFAULTS.items():
        if k.lower() == family_name.lower():
            return {
                "category": v["category"],
                "subtype": v["subtype"],
                "roles": v["roles"],
                "fallback": v["fallback"],
                "notes": None
            }
    fn_low = family_name.lower()
    if any(k in fn_low for k in ['sans', 'gothic', 'grotesk']):
        cat = "sans-serif"; sub = "grotesque"; roles = ["heading", "body", "ui"]; fb = FALLBACK_SANS
    elif any(k in fn_low for k in ['serif', 'roman', 'antiqua']):
        cat = "serif"; sub = "transitional"; roles = ["heading", "body"]; fb = FALLBACK_SERIF
    elif any(k in fn_low for k in ['script', 'hand', 'brush', 'chalk', 'pen']):
        cat = "handwriting"; sub = "casual-script"; roles = ["display", "accent"]; fb = FALLBACK_HANDWRITING
    elif any(k in fn_low for k in ['mono', 'code', 'pixel']):
        cat = "monospace"; sub = "monospace"; roles = ["code", "display"]; fb = FALLBACK_MONO
    else:
        cat = "display"; sub = "decorative-headline"; roles = ["display", "heading"]; fb = FALLBACK_DISPLAY
    return {
        "category": cat,
        "subtype": sub,
        "roles": roles,
        "fallback": fb,
        "notes": None
    }

def get_package_license_improved(source_packages, pkg_fonts):
    texts = []
    ref_files = []
    
    for pkg_name in source_packages:
        pkg_path = os.path.join(FONTS_DIR, pkg_name)
        for root, dirs, files in os.walk(pkg_path):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                rel = os.path.relpath(os.path.join(root, f), pkg_path).replace('\\', '/')
                if ext in ['.txt', '.md', '.rtf', '.html']:
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as tf:
                            texts.append(tf.read().lower())
                            ref_files.append(f"All fonts/{pkg_name}/{rel}")
                    except Exception:
                        pass
                elif ext in ['.docx', '.pdf']:
                    ref_files.append(f"All fonts/{pkg_name}/{rel}")
                    texts.append(f"filename: {f.lower()}")
                    
    meta_lic_desc = " ".join([f.get('license_desc') or '' for f in pkg_fonts]).lower()
    meta_lic_url = " ".join([f.get('license_url') or '' for f in pkg_fonts]).lower()
    meta_cp = " ".join([f.get('copyright') or '' for f in pkg_fonts]).lower()
    
    combined = " ".join(texts) + " " + meta_lic_desc + " " + meta_lic_url + " " + meta_cp
    
    if "creative commons zero" in combined or "cc0 1.0" in combined or "cc0 legal code" in combined:
        return {"type": "Creative Commons Zero 1.0 (CC0)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://creativecommons.org/publicdomain/zero/1.0/"}
    if "public domain" in combined:
        return {"type": "Public Domain Dedication", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": None}
    if "sil open font license" in combined or "scripts.sil.org/ofl" in combined or any("ofl" in rf.lower() or "open font license" in rf.lower() for rf in ref_files):
        return {"type": "SIL Open Font License 1.1 (OFL)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://scripts.sil.org/OFL"}
    if "itf free font license" in combined or any("ffl" in rf.lower() for rf in ref_files):
        return {"type": "ITF Free Font License (Fontshare FFL 2.0)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://www.fontshare.com/licensing"}
    if "ubuntu font licence" in combined or "launchpad.net/ufl" in combined:
        return {"type": "Ubuntu Font Licence 1.0", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://ubuntu.com/legal/font-licence"}
    if "1001fonts free for commercial use" in combined or any("1001fonts" in rf.lower() for rf in ref_files):
        return {"type": "1001Fonts Free Commercial License (FFC)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://www.1001fonts.com/licenses/ffc.html"}
    if "apache" in combined:
        return {"type": "Apache License 2.0", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": "https://www.apache.org/licenses/LICENSE-2.0"}
    if "baedal minjok" in combined or "woowahan" in combined:
        return {"type": "Baedal Minjok Open License", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": None}
    if "courbe sans - free standard license" in combined:
        return {"type": "Courbe Sans Free Standard License", "commercial_use": True, "redistribution_allowed": True, "risk_level": "permissive", "reference_files": ref_files, "license_url": None}
    if "nimavisual" in combined:
        return {"type": "NimaVisual EULA (No Redistribution)", "commercial_use": False, "redistribution_allowed": False, "risk_level": "restricted", "reference_files": ref_files, "license_url": "http://be.net/NimaVisual"}
    if "eimantas" in combined or "paškonis" in combined or "paskonis" in combined:
        return {"type": "Eimantas Paškonis EULA (Commercial OK, No File Sharing)", "commercial_use": True, "redistribution_allowed": False, "risk_level": "restricted", "reference_files": ref_files, "license_url": None}
    if "thanks.txt" in " ".join(ref_files).lower() and "full version" in combined:
        return {"type": "Evaluation / Demo Cut (Commercial Purchase Required)", "commercial_use": False, "redistribution_allowed": False, "risk_level": "restricted", "reference_files": ref_files, "license_url": "https://ffeeaarr.my.id/"}
    if "letterlays" in combined or any("full license.pdf" in rf.lower() for rf in ref_files):
        return {"type": "Letterlays Commercial License (Receipt PDF)", "commercial_use": True, "redistribution_allowed": False, "risk_level": "commercial_proof_needed", "reference_files": ref_files, "license_url": "https://letterlays.com"}
    if "creativefabrica" in combined:
        return {"type": "Creative Fabrica Commercial License", "commercial_use": True, "redistribution_allowed": False, "risk_level": "commercial_proof_needed", "reference_files": ref_files, "license_url": "https://www.creativefabrica.com"}
    if "befonts.com" in combined and "commercial use allowed" in combined:
        return {"type": "Freeware (Commercial Use Allowed - Befonts Grant)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": "https://befonts.com"}
    if "aluyeah studio" in combined and ("personal and commercial" in combined or "personal & commercial" in combined):
        return {"type": "Freeware (Personal & Commercial - Aluyeah Studio Grant)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": "https://aluyeah.com"}
    if "commercial use for everyone" in combined:
        return {"type": "Freeware (Commercial Use For Everyone - Author Grant)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}
    if "free made whatever you want" in combined:
        return {"type": "Freeware (Free Commercial - Author Grant)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}
    if "100% free for personal use & commercial use" in combined or "free for personal use & commercial use" in combined or "100% free for personal use and commercial use" in combined:
        return {"type": "Freeware (Personal & Commercial Use Granted)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}
    if "free for anything you want to do" in combined or "100% free open license" in combined:
        return {"type": "Freeware (Free Commercial - Author Grant)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}
    if "freeware fonts for a freeware world" in combined or "use it to your hearts content" in combined:
        return {"type": "Freeware (Author Freeware Grant)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}
    if "freeware" in combined:
        return {"type": "Freeware (General)", "commercial_use": True, "redistribution_allowed": True, "risk_level": "freeware", "reference_files": ref_files, "license_url": None}
    if meta_cp.strip():
        return {"type": f"Unspecified Copyright ({meta_cp.strip()[:60]})", "commercial_use": False, "redistribution_allowed": False, "risk_level": "unknown", "reference_files": ref_files, "license_url": None}
    return {"type": "Unknown (No License Document or Metadata)", "commercial_use": False, "redistribution_allowed": False, "risk_level": "unknown", "reference_files": ref_files, "license_url": None}

def main():
    print("Building canonical font intelligence catalog...")
    
    existing_catalog_by_id = {}
    for candidate_dir in TARGET_DIRS:
        cand_path = os.path.join(candidate_dir, "fonts.json")
        if os.path.exists(cand_path):
            try:
                with open(cand_path, 'r', encoding='utf-8') as f:
                    old_data = json.load(f)
                    for font_item in old_data.get('fonts', []):
                        existing_catalog_by_id[font_item['id']] = font_item
                print(f"Loaded {len(existing_catalog_by_id)} existing font entries for metadata preservation.")
                break
            except Exception as e:
                print(f"Note: Could not read existing catalog ({e})")
                
    pkg_dirs = sorted([d for d in os.listdir(FONTS_DIR) if os.path.isdir(os.path.join(FONTS_DIR, d))])
    print(f"Processing {len(pkg_dirs)} source packages...")
    
    family_groups = defaultdict(lambda: {
        'name': None,
        'aliases': set(),
        'source_packages': set(),
        'files': [],
        'fonts_meta': []
    })
    
    for pkg_name in pkg_dirs:
        pkg_path = os.path.join(FONTS_DIR, pkg_name)
        for root, dirs, files in os.walk(pkg_path):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                f_abs = os.path.join(root, f)
                rel_repo_path = os.path.relpath(f_abs, ROOT_DIR).replace('\\', '/')
                
                if ext in ['.ttf', '.otf', '.woff', '.woff2', '.eot']:
                    meta = {
                        'path': rel_repo_path,
                        'filename': f,
                        'format': ext.lstrip('.'),
                        'size_bytes': os.path.getsize(f_abs),
                        'sha256': get_file_sha256(f_abs),
                        'family': None,
                        'subfamily': None,
                        'weight': 400,
                        'style': 'normal',
                        'variable': False,
                        'axes': [],
                        'features': [],
                        'scripts': [],
                        'languages': [],
                        'unicode_blocks': [],
                        'total_glyphs': 0,
                        'designer': None,
                        'designer_url': None,
                        'manufacturer': None,
                        'vendor_url': None,
                        'version': None,
                        'copyright': None,
                        'license_desc': None,
                        'license_url': None,
                        'fs_type': None
                    }
                    
                    try:
                        font = fontTools.ttLib.TTFont(f_abs, lazy=True)
                        if 'maxp' in font:
                            meta['total_glyphs'] = font['maxp'].numGlyphs
                            
                        if 'OS/2' in font:
                            os2 = font['OS/2']
                            meta['weight'] = getattr(os2, 'usWeightClass', 400)
                            meta['fs_type'] = getattr(os2, 'fsType', 0)
                            fs_sel = getattr(os2, 'fsSelection', 0)
                            if (fs_sel & 0x01) or (fs_sel & 0x200):
                                meta['style'] = 'italic'
                                
                        if 'head' in font:
                            if font['head'].macStyle & 0x02:
                                meta['style'] = 'italic'
                                
                        if 'name' in font:
                            names = font['name'].names
                            meta['family'] = get_name_record(names, 16) or get_name_record(names, 1)
                            meta['subfamily'] = get_name_record(names, 17) or get_name_record(names, 2)
                            meta['designer'] = get_name_record(names, 9)
                            meta['designer_url'] = get_name_record(names, 12)
                            meta['manufacturer'] = get_name_record(names, 8)
                            meta['vendor_url'] = get_name_record(names, 11)
                            meta['version'] = get_name_record(names, 5)
                            meta['copyright'] = get_name_record(names, 0)
                            meta['license_desc'] = get_name_record(names, 13)
                            meta['license_url'] = get_name_record(names, 14)
                            
                        subf = (meta['subfamily'] or '').lower()
                        if 'italic' in subf or 'oblique' in subf or 'ital' in subf:
                            meta['style'] = 'italic'
                            
                                             
                        if 'fvar' in font:
                            meta['variable'] = True
                            fvar = font['fvar']
                            for axis in fvar.axes:
                                axis_name = None
                                if 'name' in font and hasattr(axis, 'axisNameID'):
                                    axis_name = get_name_record(font['name'].names, axis.axisNameID)
                                meta['axes'].append({
                                    'tag': axis.axisTag,
                                    'name': axis_name or axis.axisTag,
                                    'min': float(axis.minValue),
                                    'default': float(axis.defaultValue),
                                    'max': float(axis.maxValue)
                                })
                                
                        feats, ot_scripts = extract_features_and_scripts(font)
                        cp_count, blocks, u_scripts, langs = extract_unicode_info(font)
                        meta['features'] = feats
                        meta['scripts'] = sorted(list(set(u_scripts + [s for s in ot_scripts if s not in ['DFLT', 'dflt']])))
                        meta['languages'] = langs
                        meta['unicode_blocks'] = blocks
                        
                        font.close()
                    except Exception as e:
                                          
                        if 'Chillax' in f: meta['family'] = 'Chillax'
                        elif 'GeneralSans' in f: meta['family'] = 'General Sans'
                        else: meta['family'] = pkg_name
                        
                    canonical_family = resolve_canonical_family_name(meta['family'], pkg_name, f)
                    
                    fam_entry = family_groups[canonical_family]
                    fam_entry['name'] = canonical_family
                    fam_entry['source_packages'].add(pkg_name)
                    
                    if pkg_name != canonical_family:
                        fam_entry['aliases'].add(pkg_name)
                    if meta.get('family') and meta['family'] != canonical_family:
                        fam_entry['aliases'].add(meta['family'])
                        
                    fam_entry['files'].append({
                        'path': rel_repo_path,
                        'format': meta['format'],
                        'weight': meta['weight'],
                        'style': meta['style'],
                        'variable': meta['variable'],
                        'size_bytes': meta['size_bytes'],
                        'sha256': meta['sha256']
                    })
                    fam_entry['fonts_meta'].append(meta)

    print(f"Aggregated into {len(family_groups)} canonical font families.")
    
    catalog_fonts = []
    
    for fam_name, fam_data in sorted(family_groups.items(), key=lambda x: x[0].lower()):
        font_id = normalize_font_id(fam_name)
        if not font_id:
            font_id = "font-" + hashlib.md5(fam_name.encode('utf-8')).hexdigest()[:8]
            
        metas = fam_data['fonts_meta']
        pkgs = sorted(list(fam_data['source_packages']))
        
        all_weights = sorted(list(set(m['weight'] for m in metas if m['weight'] is not None)))
        if not all_weights: all_weights = [400]
        
        has_italic = any(m['style'] == 'italic' for m in metas)
        has_variable = any(m['variable'] for m in metas)
        
        var_axes = []
        for m in metas:
            if m['axes']:
                var_axes = m['axes']
                break
                
        all_scripts = sorted(list(set(s for m in metas for s in m['scripts'])))
        if not all_scripts: all_scripts = ["Latin"]
        all_languages = sorted(list(set(l for m in metas for l in m['languages'])))
        if not all_languages: all_languages = ["en"]
        all_blocks = sorted(list(set(b for m in metas for b in m['unicode_blocks'])))
        all_features = sorted(list(set(f for m in metas for f in m['features'])))
        total_glyphs = max([m['total_glyphs'] for m in metas] + [0])
        
        fs_types = set(m['fs_type'] for m in metas if m['fs_type'] is not None)
        primary_fst = max(fs_types) if fs_types else 0
        embedding_str = format_fs_type(primary_fst)
        
        designer = next((m['designer'] for m in metas if m['designer']), None)
        manufacturer = next((m['manufacturer'] for m in metas if m['manufacturer']), None)
        designer_url = next((m['designer_url'] for m in metas if m['designer_url']), None)
        vendor_url = next((m['vendor_url'] for m in metas if m['vendor_url']), None)
        version = next((m['version'] for m in metas if m['version']), None)
        copyright_str = next((m['copyright'] for m in metas if m['copyright']), None)
        
        lic_info = get_package_license_improved(pkgs, metas)
        
                                                 
        existing_item = existing_catalog_by_id.get(font_id)
        curated_info = get_curated_info(fam_name, existing_item.get('curated') if existing_item else None)
        
        aliases = sorted(list(fam_data['aliases']))
        
        font_obj = {
            "id": font_id,
            "name": fam_name,
            "aliases": aliases,
            "curated": curated_info,
            "technical": {
                "weights": all_weights,
                "italic": has_italic,
                "variable": has_variable,
                "axes": var_axes,
                "scripts": all_scripts,
                "languages": all_languages,
                "unicode_blocks": all_blocks,
                "total_glyphs": total_glyphs,
                "opentype_features": all_features,
                "embedding_permission": embedding_str
            },
            "files": fam_data['files'],
            "provenance": {
                "source_packages": pkgs,
                "designer": designer,
                "manufacturer": manufacturer,
                "designer_url": designer_url,
                "vendor_url": vendor_url,
                "version": version,
                "copyright": copyright_str
            },
            "license": lic_info
        }
        catalog_fonts.append(font_obj)
        
    full_catalog = {
        "$schema": "./fonts.schema.json",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "font-intelligence-catalog-builder/1.0.0",
        "total_families": len(catalog_fonts),
        "fonts": catalog_fonts
    }
    
                                  
    print("Validating generated catalog against schema...")
    jsonschema.validate(instance=full_catalog, schema=SCHEMA)
    print("VALIDATION SUCCESSFUL: Catalog strictly conforms to JSON schema.")
    
                              
    for target_dir in TARGET_DIRS:
        os.makedirs(target_dir, exist_ok=True)
        schema_file = os.path.join(target_dir, "fonts.schema.json")
        fonts_file = os.path.join(target_dir, "fonts.json")
        
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(SCHEMA, f, indent=2)
            
        with open(fonts_file, 'w', encoding='utf-8') as f:
            json.dump(full_catalog, f, indent=2)
            
        print(f"Written: {fonts_file} ({os.path.getsize(fonts_file):,} bytes)")
        print(f"Written: {schema_file} ({os.path.getsize(schema_file):,} bytes)")

if __name__ == '__main__':
    main()
