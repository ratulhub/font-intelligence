#!/usr/bin/env python3
"""
test_licensing.py - Unit test suite for licensing audits, redistribution safety, and embedding permissions.
"""

import os
import sys
import json
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog", "fonts.json")

class TestLicensing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

    def test_all_fonts_have_license_tracking(self):
        """Verify every font has a structured license and tracking block."""
        for font in self.catalog["fonts"]:
            lic = font.get("license", {})
            self.assertIn("type", lic, f"Font {font['id']} missing license type")
            self.assertIn("tracking", lic, f"Font {font['id']} missing license tracking")
            tracking = lic["tracking"]
            self.assertIn(tracking.get("verification_status"), ["verified", "needs-review", "restricted", "unknown"],
                          f"Font {font['id']} has invalid verification status: {tracking.get('verification_status')}")

    def test_restricted_fonts_not_marked_redistributable(self):
        """Ensure restricted or unknown fonts are never marked as safe to redistribute."""
        for font in self.catalog["fonts"]:
            tracking = font.get("license", {}).get("tracking", {})
            status = tracking.get("verification_status")
            if status in ["restricted", "unknown"]:
                self.assertFalse(tracking.get("redistribution", False),
                                 f"Restricted font {font['id']} cannot be marked as redistributable!")

    def test_office_embeddability_flagged(self):
        """Ensure embedding permissions are extracted from OS/2 table."""
        for font in self.catalog["fonts"]:
            embedding = font["technical"].get("embedding_permission")
            self.assertIsNotNone(embedding, f"Font {font['id']} missing embedding_permission")

if __name__ == "__main__":
    unittest.main()
