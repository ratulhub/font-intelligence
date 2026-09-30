import unittest
import os
import json

class TestWebEndpointsAndAssets(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.site_dir = os.path.join(self.root_dir, "site")

    def test_site_folder_exists(self):
        self.assertTrue(os.path.isdir(self.site_dir), "site/ directory must exist")

    def test_required_site_files_exist(self):
        required_files = [
            "index.html",
            "site.css",
            "site.js",
            "robots.txt",
            "sitemap.xml",
            "llms.txt",
            "llms-full.txt",
            "vercel.json",
            "docs/index.html",
            "docs.html",
            "preview/index.html",
            "README.md"
        ]
        for rel_path in required_files:
            full_path = os.path.join(self.site_dir, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Missing file in site/: {rel_path}")

    def test_root_is_clean_of_vercel_artifacts(self):
        artifacts = [
            "index.html",
            "site.css",
            "site.js",
            "robots.txt",
            "sitemap.xml",
            "vercel.json",
            "docs.html"
        ]
        for item in artifacts:
            full_path = os.path.join(self.root_dir, item)
            self.assertFalse(os.path.exists(full_path), f"Vercel artifact should not be in repository root: {item}")

    def test_index_html_seo_and_structure(self):
        index_path = os.path.join(self.site_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("<title>", content)
        self.assertIn('name="description"', content)
        self.assertIn('rel="canonical"', content)
        self.assertIn('name="google-site-verification"', content)
        self.assertIn('property="og:title"', content)
        self.assertIn('name="twitter:card"', content)
        self.assertIn('application/ld+json', content)
        self.assertIn('href="site.css"', content)
        self.assertIn('src="site.js"', content)
        self.assertIn('id="main-content"', content)
        self.assertIn('id="vibe-studio"', content)
        self.assertIn('id="scoring"', content)
        self.assertIn('id="anti-patterns"', content)
        self.assertIn('id="zero-bloat"', content)
        self.assertIn('id="agents"', content)
        self.assertIn('id="tester"', content)

    def test_robots_txt_format(self):
        robots_path = os.path.join(self.site_dir, "robots.txt")
        with open(robots_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("User-agent: *", content)
        self.assertIn("Allow: /", content)
        self.assertIn("Sitemap:", content)

    def test_sitemap_xml_format(self):
        sitemap_path = os.path.join(self.site_dir, "sitemap.xml")
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', content)
        self.assertIn('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', content)
        self.assertIn('<loc>https://font-intelligence.vercel.app/</loc>', content)
        self.assertIn('<loc>https://font-intelligence.vercel.app/docs</loc>', content)

    def test_llms_txt_format(self):
        llms_path = os.path.join(self.site_dir, "llms.txt")
        with open(llms_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("# Font Intelligence", content)
        self.assertIn("Canonical skill file:", content)
        self.assertIn("## Hard rules", content)

    def test_vercel_json_syntax(self):
        vercel_path = os.path.join(self.site_dir, "vercel.json")
        with open(vercel_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data.get("version"), 2)
        self.assertIn("rewrites", data)
        self.assertIn("headers", data)

    def test_preview_studio_resilience(self):
        preview_html = os.path.join(self.site_dir, "preview", "index.html")
        with open(preview_html, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('<base href="/preview/">', content)
        self.assertIn('href="/preview/style.css"', content)
        self.assertIn('src="/preview/fonts-data.js"', content)
        self.assertIn('src="/preview/app.js"', content)

if __name__ == "__main__":
    unittest.main()
