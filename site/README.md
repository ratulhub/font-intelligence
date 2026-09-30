# Font Intelligence — Vercel Web Deployment

This directory contains the standalone introduction website, documentation, specimen studio, and search engine assets for Font Intelligence.

## Hosting on Vercel

1. Import the repository `https://github.com/ratulhub/font-intelligence` in your Vercel Dashboard.
2. In **Project Settings** &rarr; **Root Directory**, click **Edit** and set it to:
   ```
   site
   ```
3. Framework Preset: **Other** (Pure static HTML/CSS/JS, no build step required).
4. Click **Deploy**.

## Google Search Console Setup

1. Add your domain (e.g. `https://font-intelligence.vercel.app`) in Google Search Console.
2. Use the HTML tag verification method.
3. Paste your token into `<meta name="google-site-verification" content="...">` inside `index.html` and `docs/index.html`.
4. Submit the sitemap at `https://font-intelligence.vercel.app/sitemap.xml`.

## Directory Structure

```
site/
├── index.html           # Introduction landing page with interactive vibe-to-type engine
├── site.css             # Light editorial stylesheet
├── site.js              # Interactive engine controller
├── docs/
│   └── index.html       # Full technical documentation and reference tables
├── docs.html            # Redirect helper to /docs
├── preview/             # Interactive 413-family specimen testing studio
├── robots.txt           # Search engine crawling rules (Googlebot, Bing, AI crawlers)
├── sitemap.xml          # XML sitemap for Google Search Console
├── llms.txt             # AI agent context specification
├── llms-full.txt        # Deep technical context for LLMs
├── vercel.json          # Clean URLs, route rewrites, and caching headers
└── README.md            # This deployment guide
```
