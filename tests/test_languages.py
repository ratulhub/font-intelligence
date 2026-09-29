#!/usr/bin/env python3
"""
test_languages.py - Unit test suite for strict language/script verification and Zero Tofu policy.
"""

import os
import sys
import json
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from typography_engine import TypographyEngine

class TestLanguageSupport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = TypographyEngine()

    def test_latin_fonts_available(self):
        """Verify Latin script fonts are widely supported."""
        candidates = self.engine.find_candidates(script="Latin")
        self.assertGreaterEqual(len(candidates), 90)

    def test_zero_tofu_bangla_strict_audit(self):
        """Zero Tofu Policy: Bangla must report 0 catalog fonts and recommend verified open-source companions."""
        plan = self.engine.plan_project_typography(use_case_id="news", language="bn")
        self.assertIn("Bangla", plan["language_script_audit"]["unsupported_scripts"])
        self.assertIn("Hind Siliguri", plan["language_script_audit"]["companion_fonts"])
        self.assertIn("Noto Sans Bengali", plan["language_script_audit"]["companion_fonts"])

    def test_arabic_zero_tofu_audit(self):
        """Zero Tofu Policy: Arabic must report 0 catalog fonts and recommend verified open-source companions."""
        plan = self.engine.plan_project_typography(use_case_id="news", language="ar")
        self.assertIn("Arabic", plan["language_script_audit"]["unsupported_scripts"])
        self.assertIn("Amiri", plan["language_script_audit"]["companion_fonts"])

    def test_cyrillic_script_detection(self):
        """Verify fonts with Cyrillic character coverage in binary cmap are detected."""
        cyrillic_fonts = self.engine.find_candidates(script="Cyrillic")
        self.assertGreaterEqual(len(cyrillic_fonts), 10)
        font_ids = [f["id"] for f in cyrillic_fonts]
        self.assertIn("antapani", font_ids)
        self.assertIn("balhattan", font_ids)

if __name__ == "__main__":
    unittest.main()
