#!/usr/bin/env python3
"""
test_behavior.py - Multi-step conversational simulation testing real user behavior adaptation (Phase 59).
"""

import os
import sys
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from typography_engine import TypographyEngine


class TestRealUserBehaviorSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = TypographyEngine()

    def test_step_1_premium_mens_fashion(self):
        """Prompt 1: 'Build a premium men's fashion ecommerce site.'"""
        plan = self.engine.plan_project_typography(brief="premium men's fashion ecommerce site")
        self.assertIn(plan["use_case"]["id"], ["fashion", "ecommerce", "luxury"])
        self.assertGreaterEqual(plan["recommended_pairings"][0]["score"], 90)

    def test_step_2_expensive_not_cliche(self):
        """Prompt 2: 'Make the typography feel expensive but not cliché.'"""
        plan = self.engine.plan_project_typography(brief="fashion ecommerce", style_override="expensive, not AI-looking")
        top_pair = plan["recommended_pairings"][0]
        # Must select refined, character-rich heading, not generic flat sans
        self.assertIn(top_pair["primary_font"]["id"], ["chillax", "ithaca", "credit-valley"])

    def test_step_3_modern_sans_body_expressive_heading(self):
        """Prompt 3: 'Use a modern sans for body and a more expressive font for headings.'"""
        plan = self.engine.plan_project_typography(brief="fashion ecommerce", style_override="modern, expressive")
        top_pair = plan["recommended_pairings"][0]
        self.assertIn(top_pair["secondary_font"]["id"], ["general-sans", "ubuntu"])

    def test_step_4_editorial_vibe(self):
        """Prompt 4: 'Make it feel editorial.'"""
        plan = self.engine.plan_project_typography(use_case_id="blog", style_override="editorial")
        top_pair = plan["recommended_pairings"][0]
        score = top_pair["scores"]["overall"] if "scores" in top_pair else top_pair.get("score", 0)
        self.assertGreaterEqual(score, 88)

    def test_step_5_no_ai_generated_look(self):
        """Prompt 5: 'Make the website look premium but not AI-generated.'"""
        plan = self.engine.plan_project_typography(brief="luxury website", style_override="not AI-looking, premium")
        top_pair = plan["recommended_pairings"][0]
        p_w = top_pair["primary_font"]["weight"]
        s_w = top_pair["secondary_font"]["weight"]
        self.assertGreaterEqual(abs(p_w - s_w), 100)

    def test_step_6_bangla_version(self):
        """Prompt 6: 'Build the Bangla version.'"""
        plan = self.engine.plan_project_typography(use_case_id="ecommerce", language="bn")
        self.assertIn("Hind Siliguri", plan["language_script_audit"]["companion_fonts"])
        self.assertIn("Hind Siliguri", plan["code_snippets"]["css"])

    def test_step_7_existing_typography_protection(self):
        """Prompt 7: 'Use my existing typography system and improve it without replacing the main font.'"""
        plan = self.engine.plan_project_typography(use_case_id="ecommerce", existing_fonts=["Inter", "Roboto"])
        self.assertIn("EXISTING DESIGN SYSTEM DETECTED", plan.get("existing_fonts_notice", ""))
        self.assertIn("Inter", plan.get("existing_fonts_notice", ""))


if __name__ == "__main__":
    unittest.main()
