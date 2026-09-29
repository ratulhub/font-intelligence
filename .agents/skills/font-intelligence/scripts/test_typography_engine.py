#!/usr/bin/env python3
"""
Test Suite for Typography Decision Engine & Catalog Integrity.
Verifies all 8 steps of the user request and system requirements.
"""

import os
import sys
import unittest
import json
try:
    import jsonschema
except ImportError:
    jsonschema = None


sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from typography_engine import TypographyEngine

class TestTypographyDecisionSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = TypographyEngine()
        cls.fonts = cls.engine.fonts_catalog.get("fonts", [])
        with open(os.path.join(ROOT_DIR, "catalog", "fonts.schema.json"), 'r', encoding='utf-8') as f:
            cls.schema = json.load(f)

    def test_01_catalog_schema_and_font_count(self):
        """Step 1, 2, 3: Schema validation across all families."""
        self.assertGreaterEqual(len(self.fonts), 103, "Catalog must contain at least 103 typographic families.")
                                      
        if jsonschema:
            jsonschema.validate(instance=self.engine.fonts_catalog, schema=self.schema)

    def test_02_controlled_style_categories(self):
        """Step 1: Verify controlled style categories."""
        expected_styles = {
            "modern", "premium", "luxury", "editorial", "fashion", "technical",
            "corporate", "playful", "friendly", "classic", "futuristic", "minimal", "brutalist",
            "industrial", "organic", "artistic", "sophisticated", "bold", "restrained", "expressive",
            "quirky", "geometric", "humanist", "retro", "vintage", "grunge", "art-deco",
            "decorative", "handwritten", "clean", "expensive", "elegant", "professional"
        }
        for font in self.fonts:
            cur = font["curated"]
            self.assertIn("styles", cur, f"Font {font['id']} missing 'styles'")
            self.assertTrue(len(cur["styles"]) >= 1, f"Font {font['id']} has empty styles")
            for s in cur["styles"]:
                self.assertIn(s, expected_styles, f"Font {font['id']} has uncontrolled style: {s}")

    def test_03_typography_roles(self):
        """Step 2: Verify typography roles."""
        allowed_roles = {
            "hero", "display", "heading", "body", "ui", "UI", "button",
            "navigation", "caption", "number", "price", "code", "quote",
            "logo", "branding", "accent"
        }
        for font in self.fonts:
            cur = font["curated"]
            self.assertIn("roles", cur, f"Font {font['id']} missing 'roles'")
            self.assertTrue(len(cur["roles"]) >= 1, f"Font {font['id']} has empty roles")
            for r in cur["roles"]:
                self.assertIn(r, allowed_roles, f"Font {font['id']} has invalid role: {r}")

    def test_04_readability_properties(self):
        """Step 3: Verify readability properties (body, long-form, UI, small text, numbers)."""
        required_props = ["body", "long_form", "ui", "small_text", "numbers"]
        for font in self.fonts:
            cur = font["curated"]
            self.assertIn("readability", cur, f"Font {font['id']} missing 'readability'")
            read = cur["readability"]
            for prop in required_props:
                self.assertIn(prop, read, f"Font {font['id']} readability missing '{prop}'")
                val = read[prop]
                self.assertIsInstance(val, int, f"Font {font['id']} readability '{prop}' not int")
                self.assertTrue(1 <= val <= 10, f"Font {font['id']} readability '{prop}' out of range 1-10: {val}")

    def test_05_curated_pairings_file(self):
        """Step 4: Verify catalog/pairings.json structure and rationales."""
        pairings = self.engine.pairings_data.get("pairings", [])
        self.assertTrue(len(pairings) >= 10, "Must have at least 10 curated master pairings.")
        for p in pairings:
            self.assertIn("id", p)
            self.assertIn("name", p)
            self.assertIn("primary_font", p)
            self.assertIn("secondary_font", p)
            self.assertIn("contrast_metrics", p)
            self.assertIn("scores", p)
            self.assertIn("rationale", p)
            self.assertIn("summary", p["rationale"])
            self.assertTrue("WHY IT WORKS" in p["rationale"]["summary"], "Rationale must explain WHY it works.")

    def test_06_scoring_model_and_10_criteria(self):
        """Step 5 & 6: Verify catalog/scoring.json covers all 10 criteria."""
        scoring = self.engine.scoring_model
        weights = scoring.get("weights", {})
        expected_criteria = [
            "visual_contrast",
            "serif_sans_relationship",
            "personality",
            "readability",
            "width",
            "weight_availability",
            "role_compatibility",
            "project_style",
            "language",
            "platform"
        ]
        for crit in expected_criteria:
            self.assertIn(crit, weights, f"Scoring model missing criterion: {crit}")
            self.assertIn(crit, scoring.get("dimensions", {}), f"Scoring dimensions missing: {crit}")
        total_weight = sum(weights.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2, msg="Weights must sum to 1.0")

    def test_07_anti_patterns_detection(self):
        """Step 8: Verify anti-pattern detection for all mandatory scenarios."""
                               
        castle = self.engine.get_font("castle-chunk")
        die_nasty = self.engine.get_font("die-nasty")
        eval_bad = self.engine.evaluate_pairing(castle, die_nasty, {"secondary_role": "body"})
        ap_ids = [ap["id"] for ap in eval_bad["anti_patterns"]]
        self.assertIn("decorative-as-body", ap_ids, "Must flag decorative font used as body")
        self.assertEqual(eval_bad["grade"]["tier"], "Incompatible")

                                      
        reckoner = self.engine.get_font("reckoner")
        talero = self.engine.get_font("talero")
        eval_disp = self.engine.evaluate_pairing(reckoner, talero, {"secondary_role": "heading"})
        ap_ids_disp = [ap["id"] for ap in eval_disp["anti_patterns"]]
        self.assertIn("two-similar-display-fonts", ap_ids_disp, "Must flag two competing display fonts")

                                       
        gen_sans = self.engine.get_font("general-sans")
        gudea = self.engine.get_font("gudea")
        eval_weak = self.engine.evaluate_pairing(gen_sans, gudea, {
            "primary_weight": 400,
            "secondary_weight": 400
        })
        ap_ids_weak = [ap["id"] for ap in eval_weak["anti_patterns"]]
        self.assertIn("weak-heading-body-contrast", ap_ids_weak, "Must flag weak heading/body contrast")

                                    
        excessive_aps = self.engine.detect_anti_patterns(
            primary_font=gen_sans,
            secondary_font=gudea,
            all_family_count=4
        )
        self.assertTrue(any(ap["id"] == "excessive-font-families" for ap in excessive_aps))

                              
        lang_aps = self.engine.detect_anti_patterns(
            primary_font=self.engine.get_font("bm-dohyeon"),
            secondary_font=self.engine.get_font("aclonica"),
            target_languages=["ko"]
        )
        self.assertTrue(any(ap["id"] == "language-script-mismatch" for ap in lang_aps))

    def test_08_dynamic_pairing_not_manually_listed(self):
        """Step 7: Verify dynamic pairing of fonts not manually listed in pairings.json."""
                                                                                                        
        antapani = self.engine.get_font("antapani")
        gen_sans = self.engine.get_font("general-sans")
        res = self.engine.evaluate_pairing(antapani, gen_sans, {
            "project_style": "brutalist",
            "platform": "web"
        })
        self.assertGreaterEqual(res["scores"]["overall"], 90, "Antapani + General Sans should score high in brutalist style")
        self.assertTrue(len(res["rationale"]["summary"]) > 20)
        self.assertIn("visual_contrast_why", res["rationale"])
        self.assertIn("role_harmony_why", res["rationale"])
        self.assertIn("font_family", res["typographic_recommendation"]["h1"])
        self.assertIn("Antapani", res["typographic_recommendation"]["h1"]["font_family"])

    def test_09_engine_explains_why_pair_works(self):
        """Requirement: The engine must explain WHY a pair works."""
        chillax = self.engine.get_font("chillax")
        gen_sans = self.engine.get_font("general-sans")
        res = self.engine.evaluate_pairing(chillax, gen_sans, {"project_style": "modern"})
        rat = res["rationale"]
        self.assertTrue(any("EXCELLENT" in rat["summary"] or "SYNERGY" in rat["summary"] for _ in [1]))
        self.assertTrue(len(rat["visual_contrast_why"]) > 30)
        self.assertTrue(len(rat["role_harmony_why"]) > 30)
    def test_10_use_cases_catalog(self):
        """Verify catalog/use-cases.json coverage across Web, Apps, and Documents/Marketing."""
        ucs = self.engine.usecases_data.get("use_cases", {})
        self.assertTrue(len(ucs) >= 25, "Must support at least 25 project situations.")
        
                        
        web_cases = ["saas", "landing-page", "portfolio", "dashboard", "ecommerce", "fashion",
                     "luxury", "restaurant", "finance", "fintech", "crypto", "education",
                     "gaming", "news", "blog", "agency"]
        for wc in web_cases:
            self.assertIn(wc, ucs, f"Missing Web use case: {wc}")
            self.assertEqual(ucs[wc]["category"], "web")

                        
        app_cases = ["mobile", "flutter", "react-native", "android", "ios"]
        for ac in app_cases:
            self.assertIn(ac, ucs, f"Missing App use case: {ac}")
            self.assertEqual(ucs[ac]["category"], "app")

                          
        other_cases = ["powerpoint", "presentation", "word", "pdf", "resume", "poster", "logo", "branding", "advertisement"]
        for oc in other_cases:
            self.assertIn(oc, ucs, f"Missing Other use case: {oc}")

    def test_11_style_interpretations(self):
        """Verify style interpretation for colloquial vibe queries."""
        interp = self.engine.interpret_style("expensive, not AI-looking, clean")
        self.assertIn("Expensive / High-End Prestige", interp["matched_interpretations"])
        self.assertIn("Not AI-Looking / Bespoke Human Craft", interp["matched_interpretations"])
        self.assertIn("Clean / Frictionless Clarity", interp["matched_interpretations"])
        self.assertTrue(len(interp["preferred_categories"]) > 0)
        self.assertTrue(len(interp["typographic_rationale"]) > 50)

    def test_12_strict_language_script_filtering(self):
        """Verify strict script verification: Latin, Cyrillic, Greek."""
        all_fonts = self.engine.fonts_catalog.get("fonts", [])
        
               
        latin_fonts, unsupp_l, _ = self.engine.filter_fonts_by_script(all_fonts, ["Latin"])
        self.assertGreaterEqual(len(latin_fonts), 103, "Catalog must support Latin across families")
        self.assertEqual(len(unsupp_l), 0)

                  
        cyrillic_fonts, unsupp_c, _ = self.engine.filter_fonts_by_script(all_fonts, ["Cyrillic"])
        self.assertGreaterEqual(len(cyrillic_fonts), 18, "Catalog must have verified Cyrillic fonts")
        self.assertEqual(len(unsupp_c), 0)
        cyrillic_ids = [f["id"] for f in cyrillic_fonts]
        self.assertIn("ubuntu", cyrillic_ids)
        self.assertIn("antapani", cyrillic_ids)
        self.assertNotIn("chillax", cyrillic_ids)                              

    def test_13_never_guess_language_support(self):
        """Verify engine never guesses language support for unsupported scripts (Bangla, Arabic)."""
        all_fonts = self.engine.fonts_catalog.get("fonts", [])
        
                
        b_fonts, unsupp_b, guidance_b = self.engine.filter_fonts_by_script(all_fonts, ["Bangla"])
        self.assertEqual(len(b_fonts), 0, "No catalog fonts should be returned for Bangla")
        self.assertIn("Bangla", unsupp_b, "Bangla must be flagged as unsupported in local catalog")
        self.assertIn("Bengali", guidance_b["Bangla"])

                
        a_fonts, unsupp_a, guidance_a = self.engine.filter_fonts_by_script(all_fonts, ["Arabic"])
        self.assertEqual(len(a_fonts), 0, "No catalog fonts should be returned for Arabic")
        self.assertIn("Arabic", unsupp_a, "Arabic must be flagged as unsupported in local catalog")
        self.assertIn("Amiri", guidance_a["Arabic"])

    def test_14_platform_suitability_powerpoint(self):
        """Verify PowerPoint platform requirements: TrueType (.ttf) format and embeddable licenses."""
        plan = self.engine.plan_project_typography(
            use_case_id="powerpoint",
            style_vibe="corporate",
            platform="powerpoint"
        )
        self.assertEqual(plan["platform"], "powerpoint")
        self.assertIn("ttf", plan["platform_performance"]["preferred_formats"])
        self.assertIn("TrueType", plan["platform_performance"]["notes"])
        self.assertIn("office_embedding", plan["code_snippets"])
        self.assertIn(".ttf", plan["code_snippets"]["office_embedding"])

    def test_15_project_typography_planning_end_to_end(self):
        """Verify comprehensive project typography planning for Fintech SaaS."""
        plan = self.engine.plan_project_typography(
            use_case_id="fintech",
            style_vibe="expensive, not AI-looking",
            platform="web",
            target_scripts=["Latin"]
        )
        self.assertEqual(plan["use_case"]["id"], "fintech")
        self.assertTrue(len(plan["recommended_pairings"]) > 0)
        top_pair = plan["recommended_pairings"][0]
        self.assertGreaterEqual(top_pair["scores"]["overall"], 85)
        self.assertIn("css", plan["code_snippets"])

if __name__ == "__main__":
    unittest.main()
