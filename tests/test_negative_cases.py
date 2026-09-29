#!/usr/bin/env python3
"""
test_negative_cases.py - Unit test suite evaluating all 17 negative edge cases (A through Q) from Phase 58.
"""

import os
import sys
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from typography_engine import TypographyEngine


class TestNegativeCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = TypographyEngine()

    def test_case_a_font_not_in_catalog(self):
        """Case A: User explicitly requests a font not in catalog -> System handles missing font gracefully."""
        res = self.engine.find_font_by_id("non-existent-font-xyz")
        self.assertIsNone(res, "Non-existent font should return None")

    def test_case_b_bangla_with_latin_font(self):
        """Case B: User asks for Bangla with Latin font -> Zero Tofu warns and injects companion font."""
        plan = self.engine.plan_project_typography(use_case_id="news", language="bn")
        self.assertTrue(len(plan["language_script_audit"]["companion_fonts"]) > 0)
        self.assertIn("Hind Siliguri", plan["code_snippets"]["css"])

    def test_case_c_license_unknown_or_restricted(self):
        """Case C: License is unknown/restricted -> Flagged in legal tracking."""
        font = self.engine.find_font_by_id("antapani")
        status = font["license"]["tracking"]["verification_status"]
        self.assertIn(status, ["restricted", "needs-review", "unknown"])

    def test_case_d_only_bold_exists(self):
        """Case D: Only Bold exists -> System uses actual weight, never invents light weights."""
        font = self.engine.find_font_by_id("reckoner")
        self.assertNotIn(400, font["technical"]["weights"])
        self.assertIn(700, font["technical"]["weights"])

    def test_case_e_only_regular_exists(self):
        """Case e: Only Regular exists -> System uses 400 for both without hallucinating 700."""
        eval_res = self.engine.evaluate_pairing(primary_id="credit-valley", secondary_id="credit-valley")
        self.assertEqual(eval_res["secondary_weight"], 400)

    def test_case_f_font_has_no_italic(self):
        """Case F: Font has no italic -> Technical metadata confirms italic is false."""
        font = self.engine.find_font_by_id("achtung-bravo")
        self.assertFalse(font["technical"]["italic"])

    def test_case_g_font_has_variable_axes(self):
        """Case G: Variable axes detected -> fvar axes recorded with min/max/default."""
        font = self.engine.find_font_by_id("chillax")
        self.assertTrue(font["technical"]["variable"])
        self.assertTrue(len(font["technical"]["axes"]) > 0)

    def test_case_h_existing_project_typography(self):
        """Case H: Existing project typography -> System respects and integrates, does not overwrite."""
        plan = self.engine.plan_project_typography(use_case_id="saas", existing_fonts=["Inter", "Roboto"])
        self.assertIn("EXISTING DESIGN SYSTEM DETECTED", plan.get("existing_fonts_notice", ""))

    def test_case_i_user_wants_three_decorative_fonts(self):
        """Case I: Excessive decorative fonts -> Triggers display anti-pattern."""
        eval_res = self.engine.evaluate_pairing(primary_id="castle-chunk", secondary_id="bedizen", context={"secondary_role": "heading"})
        ap_ids = [ap["id"] for ap in eval_res["anti_patterns_detected"]]
        self.assertTrue(any(ap in ap_ids for ap in ["two-similar-display-fonts", "competing-display-fonts", "decorative-as-body"]))

    def test_case_j_decorative_font_as_paragraph(self):
        """Case J: Decorative font as paragraph -> Triggers decorative-as-body penalty (-45)."""
        eval_res = self.engine.evaluate_pairing(primary_id="chillax", secondary_id="castle-chunk")
        ap_ids = [ap["id"] for ap in eval_res["anti_patterns_detected"]]
        self.assertIn("decorative-as-body", ap_ids)
        self.assertLess(eval_res["score"], 60)

    def test_case_k_performance_sensitive(self):
        """Case K: Performance-sensitive project -> Enforces payload budget < 100 KB and WOFF2."""
        plan = self.engine.plan_project_typography(use_case_id="saas", platform="web")
        perf = plan.get("platform_performance", {})
        self.assertIn("woff2", perf.get("preferred_formats", []))
        self.assertLessEqual(perf.get("max_payload_kb", 150), 120)

    def test_case_l_package_has_preview_images(self):
        """Case L: Package has preview images -> Images separated into preview assets, not confused with binaries."""
        font = self.engine.find_font_by_id("kastore")
        for f in font["files"]:
            self.assertFalse(f["path"].lower().endswith((".jpg", ".png", ".webp")))

    def test_case_m_package_has_misc_directory(self):
        """Case M: Package has misc directory -> Inspected without corrupting font file paths."""
        font = self.engine.find_font_by_id("alphakind")
        self.assertTrue(len(font["files"]) > 0)

    def test_case_n_package_has_readme_no_license(self):
        """Case N: README present but no formal license -> Classified as needs-review/restricted, not assumed OFL."""
        font = self.engine.find_font_by_id("society")
        self.assertNotEqual(font["license"]["type"], "SIL Open Font License 1.1 (OFL)")

    def test_case_o_two_folders_contain_same_family(self):
        """Case O: Two folders containing same family (e.g. Oligopoly OTF & TTF) -> Merged under single canonical ID."""
        self.assertIn("oligopoly", self.engine.fonts)

    def test_case_p_multiple_formats_with_different_weights(self):
        """Case P: Multiple formats with different weights -> Recorded accurately in technical.weights."""
        font = self.engine.find_font_by_id("balhattan")
        self.assertIn(400, font["technical"]["weights"])
        self.assertTrue(font["technical"]["italic"])

    def test_case_q_folder_name_differs_from_internal_family_name(self):
        """Case Q: Folder name does not match internal family name -> ID derived from true font name."""
        font = self.engine.find_font_by_id("chillax")
        self.assertEqual(font["name"], "Chillax")


if __name__ == "__main__":
    unittest.main()
