#!/usr/bin/env python3
"""
test_pairings.py - Unit test suite for curated pairings, 10-dimensional dynamic scoring, and anti-pattern prevention.
"""

import os
import sys
import json
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from typography_engine import TypographyEngine

PAIRINGS_PATH = os.path.join(ROOT_DIR, "catalog", "pairings.json")
SCORING_PATH = os.path.join(ROOT_DIR, "catalog", "scoring.json")
ANTI_PATTERNS_PATH = os.path.join(ROOT_DIR, "catalog", "anti-patterns.json")


class TestPairingsAndScoring(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = TypographyEngine()
        with open(PAIRINGS_PATH, "r", encoding="utf-8") as f:
            cls.pairings = json.load(f)
        with open(SCORING_PATH, "r", encoding="utf-8") as f:
            cls.scoring = json.load(f)
        with open(ANTI_PATTERNS_PATH, "r", encoding="utf-8") as f:
            cls.anti_patterns = json.load(f)

    def test_curated_pairings_valid_references(self):
        """Ensure all primary and secondary fonts in curated pairings exist in catalog."""
        font_ids = set(self.engine.fonts.keys())
        for pair in self.pairings.get("curated_pairings", []):
            pid = pair["primary_font"]["id"]
            sid = pair["secondary_font"]["id"]
            self.assertIn(pid, font_ids, f"Pairing {pair['id']} references missing primary font: {pid}")
            self.assertIn(sid, font_ids, f"Pairing {pair['id']} references missing secondary font: {sid}")

    def test_dynamic_scoring_10_dimensions(self):
        """Ensure dynamic pairing evaluates all 10 mathematical dimensions."""
        eval_res = self.engine.evaluate_pairing(primary_id="chillax", secondary_id="general-sans", style="luxury")
        self.assertGreaterEqual(eval_res["score"], 85)
        dims = eval_res["dimension_breakdown"]
        self.assertEqual(len(dims), 10, f"Expected 10 scored dimensions, got {len(dims)}")
        for dim_name in ["visual_contrast", "serif_sans_relationship", "personality",
                         "readability", "width", "weight_availability",
                         "role_compatibility", "project_style", "language", "platform"]:
            self.assertIn(dim_name, dims)

    def test_anti_pattern_penalty_decorative_body(self):
        """Setting decorative font as body must trigger severe anti-pattern penalty."""
        eval_res = self.engine.evaluate_pairing(primary_id="chillax", secondary_id="castle-chunk")
        self.assertTrue(len(eval_res["anti_patterns_detected"]) > 0)
        ap_ids = [ap["id"] for ap in eval_res["anti_patterns_detected"]]
        self.assertIn("decorative-as-body", ap_ids)
        self.assertLess(eval_res["score"], 60)


if __name__ == "__main__":
    unittest.main()
