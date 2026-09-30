#!/usr/bin/env python3
import os
import sys
import unittest
import tempfile
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from clean_project import clean_project, find_font_references_in_code

class TestCleanProject(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_font_clean_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_prune_unused_fonts(self):
        font_dir = os.path.join(self.test_dir, "public", "fonts")
        os.makedirs(font_dir, exist_ok=True)
        with open(os.path.join(font_dir, "chillax.woff2"), "wb") as f:
            f.write(b"font1")
        with open(os.path.join(font_dir, "general-sans.woff2"), "wb") as f:
            f.write(b"font2")
        with open(os.path.join(font_dir, "bloat-font.ttf"), "wb") as f:
            f.write(b"unneeded")

        res = clean_project(
            project_dir=self.test_dir,
            font_dir="public/fonts",
            keep_fonts=["chillax.woff2", "general-sans.woff2"],
            clean_skill=False
        )

        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(len(res["kept_fonts"]), 2)
        self.assertEqual(len(res["deleted_fonts"]), 1)
        self.assertTrue(os.path.exists(os.path.join(font_dir, "chillax.woff2")))
        self.assertTrue(os.path.exists(os.path.join(font_dir, "general-sans.woff2")))
        self.assertFalse(os.path.exists(os.path.join(font_dir, "bloat-font.ttf")))

    def test_clean_skill_folder(self):
        skill_dir = os.path.join(self.test_dir, ".agents", "skills", "font-intelligence")
        os.makedirs(skill_dir, exist_ok=True)
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write("temporary skill")

        res = clean_project(
            project_dir=self.test_dir,
            clean_skill=True
        )

        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(len(res["deleted_folders"]) >= 1)
        self.assertFalse(os.path.exists(skill_dir))

    def test_protected_canonical_repo(self):
        res = clean_project(
            project_dir=ROOT_DIR,
            clean_skill=True
        )
        self.assertEqual(res["status"], "PROTECTED_ROOT_ABORTED")

    def test_detect_fonts_from_css(self):
        css_dir = os.path.join(self.test_dir, "src")
        font_dir = os.path.join(self.test_dir, "fonts")
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(font_dir, exist_ok=True)

        with open(os.path.join(font_dir, "hero-bold.woff2"), "wb") as f:
            f.write(b"hero")
        with open(os.path.join(font_dir, "extra-heavy.ttf"), "wb") as f:
            f.write(b"extra")

        css_content = """
        @font-face {
            font-family: 'Hero';
            src: url('../fonts/hero-bold.woff2') format('woff2');
        }
        """
        with open(os.path.join(css_dir, "style.css"), "w") as f:
            f.write(css_content)

        res = clean_project(
            project_dir=self.test_dir,
            clean_skill=False
        )

        self.assertEqual(len(res["kept_fonts"]), 1)
        self.assertEqual(len(res["deleted_fonts"]), 1)
        self.assertTrue(os.path.exists(os.path.join(font_dir, "hero-bold.woff2")))
        self.assertFalse(os.path.exists(os.path.join(font_dir, "extra-heavy.ttf")))

if __name__ == "__main__":
    unittest.main()
