#!/usr/bin/env python3
"""
test_supporting_tools.py - Integration test suite verifying all 8 supporting Python CLI tools.
"""

import os
import sys
import unittest
import subprocess
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

def run_tool(script_name: str, args: list) -> subprocess.CompletedProcess:
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = [sys.executable, script_path] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT_DIR)

class TestSupportingPythonTools(unittest.TestCase):

    def test_01_scan_fonts_help_and_limit(self):
        """Verify scan_fonts.py --help and --limit."""
        proc_help = run_tool("scan_fonts.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)
        self.assertIn("Scan font packages", proc_help.stdout)

        proc_scan = run_tool("scan_fonts.py", ["--limit", "3", "--format", "json"])
        self.assertEqual(proc_scan.returncode, 0)
        data = json.loads(proc_scan.stdout)
        self.assertEqual(len(data), 3)
        self.assertIn("family_name", data[0])
        self.assertIn("weight", data[0])
        self.assertIn("embedding_permission", data[0])

    def test_02_build_catalog_help_and_dry_run(self):
        """Verify build_catalog.py --help and --dry-run (preserves curated fields)."""
        proc_help = run_tool("build_catalog.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)
        self.assertIn("preserving all curated fields", proc_help.stdout)

        proc_dry = run_tool("build_catalog.py", ["--dry-run"])
        self.assertEqual(proc_dry.returncode, 0)
        self.assertIn("Catalog schema validation: PASSED", proc_dry.stderr)
        self.assertIn("Preserved Curated", proc_dry.stdout)

    def test_03_search_fonts_criteria(self):
        """Verify search_fonts.py filtering by mood, role, and scripts."""
        proc_help = run_tool("search_fonts.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)

                     
        proc_mood = run_tool("search_fonts.py", ["--mood", "expensive", "--format", "json"])
        self.assertEqual(proc_mood.returncode, 0)
        mood_fonts = json.loads(proc_mood.stdout)
        self.assertTrue(len(mood_fonts) >= 1)
        font_ids = [f["id"] for f in mood_fonts]
        self.assertIn("chillax", font_ids)

                       
        proc_cyrl = run_tool("search_fonts.py", ["--script", "Cyrillic", "--format", "json"])
        self.assertEqual(proc_cyrl.returncode, 0)
        cyrl_fonts = json.loads(proc_cyrl.stdout)
        self.assertTrue(len(cyrl_fonts) >= 15)

    def test_04_recommend_project_brief(self):
        """Verify recommend.py with CLI options and JSON output."""
        proc_help = run_tool("recommend.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)

        proc_rec = run_tool("recommend.py", ["--use-case", "fintech", "--style", "expensive, not AI-looking", "--json"])
        self.assertEqual(proc_rec.returncode, 0)
        plan = json.loads(proc_rec.stdout)
        self.assertEqual(plan["use_case"]["id"], "fintech")
        self.assertTrue(len(plan["recommended_pairings"]) > 0)
        self.assertIn("css", plan["code_snippets"])

    def test_05_score_pair_10_dimensions(self):
        """Verify score_pair.py evaluates two fonts across 10 dimensions."""
        proc_help = run_tool("score_pair.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)

        proc_score = run_tool("score_pair.py", ["--primary", "chillax", "--secondary", "general-sans", "--style", "luxury", "--json"])
        self.assertEqual(proc_score.returncode, 0)
        eval_data = json.loads(proc_score.stdout)
        self.assertGreaterEqual(eval_data["scores"]["overall"], 90)
        self.assertIn("visual_contrast", eval_data["scores"]["dimensions"])
        self.assertIn("summary", eval_data["rationale"])

    def test_06_copy_fonts_dry_run_and_snippets(self):
        """Verify copy_fonts.py safely previews copy operations and generates snippets."""
        proc_help = run_tool("copy_fonts.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)

        proc_copy = run_tool("copy_fonts.py", ["--fonts", "chillax", "--dest", "dist/test-fonts", "--dry-run", "--snippets", "all"])
        self.assertEqual(proc_copy.returncode, 0)
        self.assertIn("FONT ASSET EXPORT REPORT", proc_copy.stdout)
        self.assertIn("GENERATED CSS @font-face", proc_copy.stdout)
        self.assertIn("GENERATED FLUTTER pubspec.yaml", proc_copy.stdout)

    def test_07_validate_catalog_integrity(self):
        """Verify validate_catalog.py confirms 100% path and schema validity."""
        proc_help = run_tool("validate_catalog.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)

        proc_val = run_tool("validate_catalog.py", ["--json"])
        self.assertEqual(proc_val.returncode, 0)
        report = json.loads(proc_val.stdout)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["missing_files"], [])
        self.assertEqual(report["invalid_ids"], [])
        self.assertEqual(report["duplicate_ids"], [])

    def test_08_validate_licenses_audit(self):
        """Verify validate_licenses.py detects compliance tiers and office embedding."""
        proc_help = run_tool("validate_licenses.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)

        proc_lic = run_tool("validate_licenses.py", ["--format", "json"])
        self.assertEqual(proc_lic.returncode, 0)
        report = json.loads(proc_lic.stdout)
        self.assertGreaterEqual(report["total_fonts"], 103)
        self.assertTrue(report["permissive_count"] > 50)
    def test_09_clean_project_tool(self):
        """Verify clean_project.py help and protected root execution."""
        proc_help = run_tool("clean_project.py", ["--help"])
        self.assertEqual(proc_help.returncode, 0)
        self.assertIn("Clean unneeded font files and skill folders", proc_help.stdout)

        proc_run = run_tool("clean_project.py", ["--project-dir", ROOT_DIR])
        self.assertIn("[PROTECTED]", proc_run.stderr)

if __name__ == "__main__":
    unittest.main()
