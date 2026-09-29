"""
test_recommendations.py - Test suite evaluating all 20 project cases 
"""

import os
import sys
import unittest

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from typography_engine import TypographyEngine


class TestProjectRecommendations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = TypographyEngine()

    def run_case(self, brief: str, expected_min_score: int = 80):
        plan = self.engine.plan_project_typography(brief=brief)
        self.assertIsNotNone(plan, f"Failed to generate plan for: {brief}")
        self.assertTrue(len(plan["recommended_pairings"]) > 0, f"No pairings returned for: {brief}")
        top_pair = plan["recommended_pairings"][0]
        score = top_pair["scores"]["overall"] if "scores" in top_pair else top_pair.get("score", 0)
        self.assertGreaterEqual(score, expected_min_score,
                                f"Score for {brief} was {score}, expected >= {expected_min_score}")
        self.assertTrue(len(plan["code_snippets"]) > 0)
        self.assertIn("typographic_recommendation", top_pair)
        return plan

    def test_01_luxury_fashion_website(self):
        self.run_case("luxury fashion website")

    def test_02_premium_mens_fashion_website(self):
        self.run_case("premium men's fashion ecommerce website")

    def test_03_saas_landing_page(self):
        self.run_case("SaaS landing page")

    def test_04_fintech_dashboard(self):
        self.run_case("fintech dashboard")

    def test_05_crypto_dashboard(self):
        self.run_case("crypto dashboard")

    def test_06_bangla_news_website(self):
        plan = self.run_case("Bangla news website")
        self.assertIn("Hind Siliguri", plan["language_script_audit"]["companion_fonts"])

    def test_07_bangla_ecommerce_website(self):
        plan = self.run_case("Bangla ecommerce website")
        self.assertIn("Hind Siliguri", plan["language_script_audit"]["companion_fonts"])

    def test_08_mobile_banking_app(self):
        self.run_case("mobile banking app")

    def test_09_kids_education_app(self):
        self.run_case("kids education app")

    def test_10_developer_tool(self):
        self.run_case("developer tool")

    def test_11_restaurant_website(self):
        self.run_case("restaurant website")

    def test_12_wedding_invitation(self):
        self.run_case("wedding invitation")

    def test_13_startup_pitch_deck(self):
        self.run_case("startup pitch deck")

    def test_14_university_presentation(self):
        self.run_case("university presentation")

    def test_15_editorial_magazine(self):
        self.run_case("editorial magazine")

    def test_16_portfolio(self):
        self.run_case("portfolio")

    def test_17_resume(self):
        self.run_case("resume")

    def test_18_logo_brand_identity(self):
        self.run_case("logo and brand identity")

    def test_19_pdf_report(self):
        self.run_case("PDF report")

    def test_20_mobile_app(self):
        self.run_case("mobile app")


if __name__ == "__main__":
    unittest.main()
