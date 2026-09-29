#!/usr/bin/env python3
"""
test_catalog.py - Unit test suite for catalog schema, uniqueness, and file path integrity.
"""

import os
import sys
import json
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")
SCHEMA_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.schema.json")


class TestFontCatalog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

    def test_schema_validity(self):
        """Validate fonts.json against fonts.schema.json."""
        try:
            import jsonschema
            jsonschema.validate(instance=self.catalog, schema=self.schema)
        except ImportError:
            self.skipTest("jsonschema not installed")

    def test_unique_ids(self):
        """Ensure all font IDs are unique, lowercase, and hyphenated."""
        ids = [f["id"] for f in self.catalog["fonts"]]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate font IDs discovered in catalog!")
        for fid in ids:
            self.assertEqual(fid, fid.lower(), f"ID {fid} is not lowercase")
            self.assertFalse(" " in fid, f"ID {fid} contains spaces")

    def test_physical_font_files_exist(self):
        """Ensure all font binary paths in catalog actually exist on disk."""
        missing = []
        for font in self.catalog["fonts"]:
            for f in font.get("files", []):
                full_path = os.path.join(ROOT_DIR, f["path"])
                if not os.path.exists(full_path):
                    missing.append(f["path"])
        self.assertEqual(len(missing), 0, f"Missing physical font files: {missing}")

    def test_curated_and_technical_separation(self):
        """Ensure technical facts are distinct from curated editorial analysis."""
        for font in self.catalog["fonts"]:
            self.assertIn("curated", font, f"Font {font['id']} missing curated section")
            self.assertIn("technical", font, f"Font {font['id']} missing technical section")
            self.assertIn("readability", font["curated"], f"Font {font['id']} missing readability")
            self.assertIn("weights", font["technical"], f"Font {font['id']} missing technical weights")
            self.assertTrue(len(font["technical"]["weights"]) > 0, f"Font {font['id']} has empty weights")


if __name__ == "__main__":
    unittest.main()
