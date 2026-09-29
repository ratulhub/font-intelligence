import os
import json
import jsonschema

CATALOG_DIRS = [
    r"D:\font-intelligence\catalog"
]

CONTROLLED_STYLES = [
    "modern",
    "premium",
    "luxury",
    "editorial",
    "fashion",
    "technical",
    "corporate",
    "playful",
    "classic",
    "futuristic",
    "minimal",
    "brutalist",
    "industrial",
    "geometric",
    "humanist",
    "retro",
    "vintage",
    "organic",
    "grunge",
    "art-deco",
    "decorative",
    "handwritten"
]

TYPOGRAPHY_ROLES = [
    "display",
    "hero",
    "heading",
    "body",
    "ui",
    "UI",
    "button",
    "number",
    "caption",
    "code",
    "logo",
    "branding",
    "accent"
]

                                                         
CURATION_MAP = {
    "general-sans": {
        "category": "sans-serif",
        "subtype": "geometric-neo-grotesque",
        "styles": ["modern", "minimal", "corporate", "premium", "technical"],
        "roles": ["display", "hero", "heading", "body", "ui", "button", "number", "caption"],
        "readability": {"body": 9, "long_form": 9, "ui": 10, "small_text": 9, "numbers": 9, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Premium Fontshare neo-grotesque workhorse with companion italic and variable axis. Exceptional across all UI and body text contexts."
    },
    "chillax": {
        "category": "sans-serif",
        "subtype": "geometric-contemporary",
        "styles": ["modern", "minimal", "premium", "luxury", "fashion"],
        "roles": ["display", "hero", "heading", "ui", "button", "branding", "logo"],
        "readability": {"body": 7, "long_form": 6, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "generous", "aperture": "moderate", "stroke_contrast": "low-medium", "legibility_tier": "good"}},
        "notes": "Contemporary geometric sans with stylish alternates. Superb for high-end SaaS, tech luxury, and refined headlines."
    },
    "ubuntu": {
        "category": "sans-serif",
        "subtype": "humanist",
        "styles": ["modern", "corporate", "technical", "humanist"],
        "roles": ["heading", "body", "ui", "button", "caption", "number"],
        "readability": {"body": 9, "long_form": 9, "ui": 9, "small_text": 9, "numbers": 9, "factors": {"x_height": "generous", "aperture": "wide-open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Engineered for maximum legibility on digital screens across multi-weights. Highly accessible humanist proportions."
    },
    "ubuntu-condensed": {
        "category": "sans-serif",
        "subtype": "humanist-condensed",
        "styles": ["technical", "modern", "corporate"],
        "roles": ["display", "heading", "ui", "button"],
        "readability": {"body": 6, "long_form": 5, "ui": 7, "small_text": 6, "numbers": 8, "factors": {"x_height": "high", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "moderate"}},
        "notes": "Space-saving condensed humanist display and UI headline cut."
    },
    "ubuntu-mono": {
        "category": "monospace",
        "subtype": "humanist-monospace",
        "styles": ["technical", "modern", "corporate"],
        "roles": ["code", "number", "caption", "ui"],
        "readability": {"body": 7, "long_form": 6, "ui": 8, "small_text": 8, "numbers": 10, "factors": {"x_height": "high", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "optimal-code"}},
        "notes": "Industry-standard developer code and numerical data display font with companion italic."
    },
    "credit-valley": {
        "category": "serif",
        "subtype": "transitional-serif",
        "styles": ["editorial", "classic", "corporate", "premium"],
        "roles": ["hero", "heading", "body", "caption"],
        "readability": {"body": 9, "long_form": 9, "ui": 7, "small_text": 7, "numbers": 8, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "medium", "legibility_tier": "optimal-editorial"}},
        "notes": "Refined transitional serif with true companion italic. Excellent reading cadence and classical literary authority."
    },
    "credit-river": {
        "category": "sans-serif",
        "subtype": "clean-grotesque",
        "styles": ["corporate", "modern", "classic"],
        "roles": ["display", "heading", "ui"],
        "readability": {"body": 7, "long_form": 6, "ui": 8, "small_text": 7, "numbers": 7, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Structured grotesque counterpart to Credit Valley."
    },
    "ithaca": {
        "category": "serif",
        "subtype": "high-contrast-display-serif",
        "styles": ["luxury", "editorial", "fashion", "premium", "classic"],
        "roles": ["display", "hero", "heading", "logo", "branding"],
        "readability": {"body": 3, "long_form": 2, "ui": 2, "small_text": 1, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "narrow", "stroke_contrast": "ultra-high", "legibility_tier": "display-only"}},
        "notes": "High-fashion didone serif with dramatic thick/thin stroke contrast. Commands presence in luxury and editorial headers."
    },
    "gudea": {
        "category": "sans-serif",
        "subtype": "humanist",
        "styles": ["modern", "corporate", "humanist", "editorial"],
        "roles": ["body", "heading", "ui", "caption"],
        "readability": {"body": 9, "long_form": 9, "ui": 8, "small_text": 8, "numbers": 8, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Humanist sans designed specifically for continuous long-form prose and functional UI text."
    },
    "simply-sans": {
        "category": "sans-serif",
        "subtype": "geometric",
        "styles": ["minimal", "modern", "corporate"],
        "roles": ["body", "heading", "ui", "button"],
        "readability": {"body": 8, "long_form": 8, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "balanced", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Clean geometric sans with companion italics. Provides geometric clarity without sacrificing body text rhythm."
    },
    "neris": {
        "category": "sans-serif",
        "subtype": "geometric-neo-grotesque",
        "styles": ["modern", "technical", "corporate", "minimal"],
        "roles": ["display", "hero", "heading", "body", "ui", "button"],
        "readability": {"body": 8, "long_form": 8, "ui": 9, "small_text": 8, "numbers": 8, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Versatile multi-weight system (Thin to Black with true italics). Robust across product interfaces and headlines."
    },
    "kingsbridge": {
        "category": "sans-serif",
        "subtype": "grotesque-condensed-expanded",
        "styles": ["modern", "fashion", "corporate", "editorial", "brutalist"],
        "roles": ["display", "hero", "heading", "ui", "button", "branding"],
        "readability": {"body": 7, "long_form": 6, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "generous", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Massive 44-weight typographic superfamily spanning ultra-condensed to ultra-expanded cuts."
    },
    "modestic-sans": {
        "category": "sans-serif",
        "subtype": "clean-neo-grotesque",
        "styles": ["modern", "minimal", "corporate"],
        "roles": ["heading", "body", "ui", "button"],
        "readability": {"body": 8, "long_form": 8, "ui": 8, "small_text": 8, "numbers": 8, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Modern neo-grotesque built with balanced geometric proportions."
    },
    "garute": {
        "category": "sans-serif",
        "subtype": "geometric-grotesque",
        "styles": ["modern", "corporate", "editorial"],
        "roles": ["display", "heading", "body", "ui"],
        "readability": {"body": 8, "long_form": 7, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "generous", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Extensive 7-weight sans family with oblique styles and rich specimen documentation."
    },
    "heming": {
        "category": "sans-serif",
        "subtype": "minimalist-contemporary",
        "styles": ["minimal", "modern", "editorial"],
        "roles": ["heading", "body", "ui", "caption"],
        "readability": {"body": 8, "long_form": 8, "ui": 8, "small_text": 7, "numbers": 7, "factors": {"x_height": "balanced", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Variable minimalist sans with continuous weight interpolation."
    },
    "dosis": {
        "category": "sans-serif",
        "subtype": "rounded-geometric",
        "styles": ["modern", "playful", "minimal"],
        "roles": ["display", "hero", "heading", "ui", "button"],
        "readability": {"body": 7, "long_form": 6, "ui": 7, "small_text": 6, "numbers": 7, "factors": {"x_height": "high", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "good"}},
        "notes": "Friendly rounded geometric sans with wide weight coverage from ExtraLight to ExtraBold."
    },
    "lokro": {
        "category": "sans-serif",
        "subtype": "minimalist-grotesque",
        "styles": ["minimal", "modern", "brutalist"],
        "roles": ["display", "hero", "heading", "branding"],
        "readability": {"body": 6, "long_form": 5, "ui": 6, "small_text": 5, "numbers": 7, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "moderate"}},
        "notes": "Sculpted minimalist grotesque suited for avant-garde titles and architectural posters."
    },
    "cuyabra": {
        "category": "sans-serif",
        "subtype": "humanist-sans",
        "styles": ["humanist", "modern", "corporate"],
        "roles": ["heading", "body", "ui"],
        "readability": {"body": 8, "long_form": 8, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "optimal"}},
        "notes": "Warm humanist sans with natural stroke terminals."
    },
    "newshape": {
        "category": "sans-serif",
        "subtype": "modern-grotesque",
        "styles": ["modern", "corporate", "minimal"],
        "roles": ["display", "heading", "body", "ui"],
        "readability": {"body": 8, "long_form": 7, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "balanced", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Modern grotesque with companion italic."
    },
    "newestshape": {
        "category": "sans-serif",
        "subtype": "modern-grotesque",
        "styles": ["modern", "corporate", "minimal"],
        "roles": ["display", "heading", "body", "ui"],
        "readability": {"body": 8, "long_form": 7, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "balanced", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Updated companion cut of NewShape."
    },
    "oligopoly": {
        "category": "sans-serif",
        "subtype": "geometric-modern",
        "styles": ["modern", "fashion", "premium", "luxury", "minimal"],
        "roles": ["display", "hero", "heading", "branding", "logo"],
        "readability": {"body": 6, "long_form": 5, "ui": 6, "small_text": 5, "numbers": 7, "factors": {"x_height": "generous", "aperture": "moderate", "stroke_contrast": "low-medium", "legibility_tier": "moderate"}},
        "notes": "Sharp, avant-garde geometric sans with strong fashion and corporate presence."
    },
    "courbe-sans": {
        "category": "sans-serif",
        "subtype": "high-contrast-sans",
        "styles": ["luxury", "fashion", "premium", "editorial"],
        "roles": ["display", "hero", "heading", "branding", "logo"],
        "readability": {"body": 4, "long_form": 3, "ui": 4, "small_text": 2, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "high", "legibility_tier": "display-only"}},
        "notes": "Curved high-contrast display sans ideal for haute couture, luxury cosmetics, and magazine titles."
    },
    "reckoner": {
        "category": "sans-serif",
        "subtype": "industrial-condensed",
        "styles": ["brutalist", "industrial", "technical", "modern"],
        "roles": ["display", "hero", "heading", "logo", "branding"],
        "readability": {"body": 3, "long_form": 2, "ui": 4, "small_text": 2, "numbers": 7, "factors": {"x_height": "high", "aperture": "closed", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Raw, angular industrial condensed uppercase sans. Ideal for brutalist posters and heavy hero headers."
    },
    "castle-chunk": {
        "category": "display",
        "subtype": "heavy-slab-chunky",
        "styles": ["brutalist", "playful", "retro", "industrial"],
        "roles": ["display", "hero", "heading", "logo"],
        "readability": {"body": 1, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "heavy-block", "aperture": "tight", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Monumental chunky display slab. Exclusively designed for high-impact titles and graphic branding."
    },
    "the-bold-font": {
        "category": "display",
        "subtype": "impact-all-caps",
        "styles": ["brutalist", "modern", "corporate", "industrial"],
        "roles": ["display", "hero", "heading", "button", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 3, "small_text": 2, "numbers": 7, "factors": {"x_height": "all-caps", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Classic heavy all-caps display headline typeface."
    },
    "neuropol": {
        "category": "display",
        "subtype": "futuristic-geom",
        "styles": ["futuristic", "technical", "modern"],
        "roles": ["display", "hero", "heading", "logo"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "open-geom", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Iconic futuristic sci-fi typeface created by Ray Larabie."
    },
    "unispace": {
        "category": "monospace",
        "subtype": "futuristic-monospace",
        "styles": ["futuristic", "technical", "brutalist"],
        "roles": ["display", "code", "heading", "number", "ui"],
        "readability": {"body": 5, "long_form": 4, "ui": 6, "small_text": 5, "numbers": 8, "factors": {"x_height": "high", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "moderate"}},
        "notes": "Technical monospaced font with futuristic angular geometry. Great for HUDs, dashboards, and telemetry."
    },
    "raster-forge": {
        "category": "monospace",
        "subtype": "pixel-bitmap",
        "styles": ["technical", "retro", "playful"],
        "roles": ["code", "display", "number", "ui"],
        "readability": {"body": 4, "long_form": 3, "ui": 5, "small_text": 4, "numbers": 7, "factors": {"x_height": "pixel-grid", "aperture": "grid", "stroke_contrast": "none", "legibility_tier": "pixel-only"}},
        "notes": "Authentic pixel 8-bit bitmap font for gaming, retro computing, and digital counter badges."
    },
    "jazzy-huitbits": {
        "category": "monospace",
        "subtype": "pixel-8bit",
        "styles": ["technical", "retro", "playful"],
        "roles": ["code", "display", "number"],
        "readability": {"body": 4, "long_form": 3, "ui": 5, "small_text": 4, "numbers": 7, "factors": {"x_height": "pixel-grid", "aperture": "grid", "stroke_contrast": "none", "legibility_tier": "pixel-only"}},
        "notes": "Charming retro 8-bit monospace typeface."
    },
    "zt-shago": {
        "category": "display",
        "subtype": "heavy-neo-grotesque",
        "styles": ["brutalist", "modern", "industrial", "editorial"],
        "roles": ["display", "hero", "heading", "branding"],
        "readability": {"body": 4, "long_form": 3, "ui": 4, "small_text": 3, "numbers": 7, "factors": {"x_height": "heavy-dense", "aperture": "tight", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Massive ultra-heavy display neo-grotesque scaling up to weight 950 with italics."
    },
    "talero": {
        "category": "display",
        "subtype": "futuristic-sans",
        "styles": ["futuristic", "technical", "modern"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 3, "small_text": 1, "numbers": 6, "factors": {"x_height": "high", "aperture": "closed", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Condensed futuristic sans display."
    },
    "zero-cool": {
        "category": "display",
        "subtype": "cyberpunk-techno",
        "styles": ["futuristic", "technical", "brutalist"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "moderate", "aperture": "closed", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Sharp cyberpunk display font."
    },
    "guanine": {
        "category": "display",
        "subtype": "sci-fi-techno",
        "styles": ["futuristic", "technical"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "moderate", "aperture": "geometric", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Distinctive sci-fi techno headline typeface."
    },
    "delta-block": {
        "category": "display",
        "subtype": "heavy-block-futuristic",
        "styles": ["futuristic", "brutalist", "technical"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 1, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "solid-block", "aperture": "tight", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Solid geometric block letter display font."
    },
    "unsteady-oversteer": {
        "category": "display",
        "subtype": "racing-italic-techno",
        "styles": ["futuristic", "technical", "modern"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "slanted", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "High-velocity racing italic display typeface."
    },
    "timeburner": {
        "category": "sans-serif",
        "subtype": "techno-rounded",
        "styles": ["technical", "modern", "futuristic"],
        "roles": ["display", "heading", "ui", "button"],
        "readability": {"body": 6, "long_form": 5, "ui": 7, "small_text": 6, "numbers": 8, "factors": {"x_height": "balanced", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "good"}},
        "notes": "Rounded techno sans with Bold companion."
    },
    "warriot": {
        "category": "display",
        "subtype": "condensed-esports",
        "styles": ["futuristic", "technical", "brutalist"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 6, "factors": {"x_height": "high-condensed", "aperture": "narrow", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Aggressive condensed display typeface tailored for gaming and esports."
    },
    "society": {
        "category": "display",
        "subtype": "stencil-modern",
        "styles": ["brutalist", "modern", "industrial"],
        "roles": ["display", "hero", "heading", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 3, "small_text": 1, "numbers": 6, "factors": {"x_height": "stencil-cut", "aperture": "segmented", "stroke_contrast": "medium", "legibility_tier": "display-only"}},
        "notes": "Modern stencil cuts suitable for industrial and editorial titles."
    },
    "inflammable-age": {
        "category": "display",
        "subtype": "industrial-stencil",
        "styles": ["brutalist", "industrial", "retro"],
        "roles": ["display", "hero", "heading", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "stencil-grid", "aperture": "segmented", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Industrial shipping-crate stencil typeface."
    },
    "bedizen": {
        "category": "display",
        "subtype": "decorative-headline",
        "styles": ["brutalist", "industrial", "modern"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Angular modern display headline font."
    },
    "antapani": {
        "category": "display",
        "subtype": "heavy-grotesque-display",
        "styles": ["brutalist", "modern", "industrial"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "high", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Extra-bold display grotesque."
    },
    "wide-road": {
        "category": "display",
        "subtype": "ultra-extended-highway",
        "styles": ["brutalist", "industrial", "modern"],
        "roles": ["display", "hero", "heading", "branding"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 6, "factors": {"x_height": "wide-extended", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Ultra-extended geometric headline font inspired by highway signage."
    },
    "bjorn": {
        "category": "display",
        "subtype": "nordic-uppercase",
        "styles": ["minimal", "modern", "brutalist"],
        "roles": ["display", "hero", "heading", "branding"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "all-caps", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Clean Nordic uppercase display sans with distinctive crossbars."
    },
    "al-saflers": {
        "category": "display",
        "subtype": "stylish-modern-display",
        "styles": ["fashion", "luxury", "editorial", "modern"],
        "roles": ["display", "hero", "heading", "logo", "branding"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "styled", "stroke_contrast": "medium", "legibility_tier": "display-only"}},
        "notes": "Contemporary fashion-forward headline typeface."
    },
    "lumierepolis": {
        "category": "display",
        "subtype": "art-deco-display",
        "styles": ["art-deco", "luxury", "retro", "classic"],
        "roles": ["display", "hero", "heading", "logo"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "art-deco-scale", "aperture": "decorative", "stroke_contrast": "medium", "legibility_tier": "display-only"}},
        "notes": "Vintage Art Deco display typeface with multiple weights."
    },
    "styllo": {
        "category": "display",
        "subtype": "decorative-headline",
        "styles": ["fashion", "luxury", "modern", "premium"],
        "roles": ["display", "hero", "heading", "branding"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "stylish", "stroke_contrast": "medium", "legibility_tier": "display-only"}},
        "notes": "High-contrast stylish headline typeface."
    },
    "bm-dohyeon": {
        "category": "sans-serif",
        "subtype": "hangul-retro-grotesque",
        "styles": ["retro", "editorial", "modern"],
        "roles": ["display", "hero", "heading", "logo"],
        "readability": {"body": 6, "long_form": 5, "ui": 6, "small_text": 5, "numbers": 8, "factors": {"x_height": "high", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "moderate"}},
        "notes": "Popular Korean display font inspired by classic acrylic advertising typography with full Hangul character support."
    },
    "viga": {
        "category": "sans-serif",
        "subtype": "display-sans",
        "styles": ["modern", "editorial", "geometric"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 6, "long_form": 5, "ui": 6, "small_text": 5, "numbers": 7, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Well-balanced display sans with personality."
    },
    "balhattan": {
        "category": "sans-serif",
        "subtype": "condensed-grotesque",
        "styles": ["modern", "corporate", "editorial"],
        "roles": ["display", "heading", "ui"],
        "readability": {"body": 6, "long_form": 5, "ui": 6, "small_text": 5, "numbers": 7, "factors": {"x_height": "high", "aperture": "moderate", "stroke_contrast": "low", "legibility_tier": "good"}},
        "notes": "Clean condensed grotesque sans."
    },
    "bakula": {
        "category": "handwriting",
        "subtype": "brush-handwritten",
        "styles": ["handwritten", "organic", "playful", "editorial"],
        "roles": ["display", "hero", "accent", "branding", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "irregular", "aperture": "brush", "stroke_contrast": "expressive", "legibility_tier": "accent-only"}},
        "notes": "Expressive dry-brush script with genuine hand-painted texture."
    },
    "alphakind": {
        "category": "handwriting",
        "subtype": "friendly-casual-hand",
        "styles": ["playful", "handwritten", "organic"],
        "roles": ["display", "hero", "heading", "accent", "branding"],
        "readability": {"body": 4, "long_form": 3, "ui": 3, "small_text": 2, "numbers": 5, "factors": {"x_height": "casual", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "accent-only"}},
        "notes": "Friendly, welcoming handwriting script."
    },
    "sweet-school": {
        "category": "handwriting",
        "subtype": "cute-chalk-hand",
        "styles": ["playful", "handwritten", "retro"],
        "roles": ["display", "accent", "branding"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "casual", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "accent-only"}},
        "notes": "Charming chalkboard-style casual handwriting."
    },
    "biocats": {
        "category": "handwriting",
        "subtype": "casual-organic-script",
        "styles": ["playful", "handwritten", "organic"],
        "roles": ["display", "accent", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "script", "aperture": "loop", "stroke_contrast": "variable", "legibility_tier": "accent-only"}},
        "notes": "Organic playful brush lettering."
    },
    "anak-bijak": {
        "category": "handwriting",
        "subtype": "playful-kids-script",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "childlike", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "accent-only"}},
        "notes": "Playful children book script."
    },
    "anak-gedong": {
        "category": "handwriting",
        "subtype": "playful-marker",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "casual", "aperture": "open", "stroke_contrast": "marker", "legibility_tier": "accent-only"}},
        "notes": "Casual marker pen script."
    },
    "pingsan": {
        "category": "handwriting",
        "subtype": "quirky-doodle",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 3, "factors": {"x_height": "quirky", "aperture": "irregular", "stroke_contrast": "none", "legibility_tier": "accent-only"}},
        "notes": "Quirky hand-doodled typography."
    },
    "halo-dek": {
        "category": "handwriting",
        "subtype": "friendly-marker",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent", "branding"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "marker", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "accent-only"}},
        "notes": "Friendly casual marker lettering."
    },
    "spicy-sale": {
        "category": "handwriting",
        "subtype": "bold-promo-script",
        "styles": ["playful", "handwritten", "retro"],
        "roles": ["display", "accent", "branding"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "bold-script", "aperture": "loop", "stroke_contrast": "medium", "legibility_tier": "accent-only"}},
        "notes": "Punchy promotional script lettering for sales and badges."
    },
    "butflow": {
        "category": "handwriting",
        "subtype": "flowing-script",
        "styles": ["handwritten", "luxury", "fashion", "organic"],
        "roles": ["display", "accent", "branding", "logo"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 3, "factors": {"x_height": "cursive", "aperture": "loop", "stroke_contrast": "high", "legibility_tier": "accent-only"}},
        "notes": "Elegant flowing cursive script."
    },
    "jumping-chick": {
        "category": "handwriting",
        "subtype": "cute-cartoon",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "cartoon", "aperture": "bubbly", "stroke_contrast": "none", "legibility_tier": "accent-only"}},
        "notes": "Whimsical cartoon display lettering."
    },
    "super-joyful": {
        "category": "handwriting",
        "subtype": "childish-comic",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "comic", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "accent-only"}},
        "notes": "Joyful comic lettering."
    },
    "super-malibu": {
        "category": "handwriting",
        "subtype": "retro-beach-hand",
        "styles": ["playful", "handwritten", "retro"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "retro-hand", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "accent-only"}},
        "notes": "Casual retro summer beach hand."
    },
    "super-starfish": {
        "category": "handwriting",
        "subtype": "bubbly-casual",
        "styles": ["playful", "handwritten"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "bubbly", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "accent-only"}},
        "notes": "Bubbly casual handwritten script."
    },
    "die-nasty": {
        "category": "display",
        "subtype": "grunge-distressed",
        "styles": ["grunge", "brutalist", "retro"],
        "roles": ["display", "hero", "accent", "logo"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "distressed", "aperture": "eroded", "stroke_contrast": "irregular", "legibility_tier": "distressed-only"}},
        "notes": "Heavily distressed punk grunge display font."
    },
    "ruthless-sketch": {
        "category": "display",
        "subtype": "crosshatch-sketch",
        "styles": ["grunge", "brutalist", "decorative"],
        "roles": ["display", "hero", "accent"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "hatched", "aperture": "sketchy", "stroke_contrast": "textured", "legibility_tier": "sketch-only"}},
        "notes": "Crosshatched sketch display font."
    },
    "paint-marker": {
        "category": "display",
        "subtype": "paint-graffiti",
        "styles": ["grunge", "playful", "brutalist"],
        "roles": ["display", "hero", "accent", "branding"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "dripping", "aperture": "graffiti", "stroke_contrast": "dripping", "legibility_tier": "display-only"}},
        "notes": "Urban graffiti street paint marker lettering."
    },
    "stampcraft": {
        "category": "display",
        "subtype": "rubber-stamp",
        "styles": ["grunge", "retro", "vintage"],
        "roles": ["display", "hero", "accent"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 4, "factors": {"x_height": "stamped", "aperture": "eroded", "stroke_contrast": "textured", "legibility_tier": "display-only"}},
        "notes": "Weathered rubber-stamp texture display."
    },
    "street-cred": {
        "category": "display",
        "subtype": "urban-graffiti",
        "styles": ["grunge", "playful", "brutalist"],
        "roles": ["display", "hero", "accent"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "graffiti-tag", "aperture": "closed", "stroke_contrast": "spray", "legibility_tier": "display-only"}},
        "notes": "Urban spray paint graffiti tag font."
    },
    "jogrunge": {
        "category": "display",
        "subtype": "grunge-distressed",
        "styles": ["grunge", "brutalist", "retro"],
        "roles": ["display", "hero", "accent"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "distressed", "aperture": "eroded", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Textured grunge headline display."
    },
    "free-cheese": {
        "category": "display",
        "subtype": "novelty-comic",
        "styles": ["playful", "retro", "decorative"],
        "roles": ["display", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "novelty", "aperture": "round", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Novelty comic cartoon lettering."
    },
    "vaticanus": {
        "category": "display",
        "subtype": "monumental-blackletter",
        "styles": ["classic", "vintage", "decorative"],
        "roles": ["display", "hero", "accent", "logo"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 4, "factors": {"x_height": "blackletter", "aperture": "dense", "stroke_contrast": "high", "legibility_tier": "display-only"}},
        "notes": "Classical Gothic blackletter with monumental flourishes."
    },
    "zorque": {
        "category": "display",
        "subtype": "chunky-arcade",
        "styles": ["playful", "retro", "futuristic"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "arcade-slab", "aperture": "tight", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Chunky arcade video game display."
    },
    "zt-nature": {
        "category": "display",
        "subtype": "botanical-organic",
        "styles": ["organic", "decorative", "editorial"],
        "roles": ["display", "hero", "heading", "accent"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "organic-branch", "aperture": "stylized", "stroke_contrast": "variable", "legibility_tier": "display-only"}},
        "notes": "Botanical floral leaf-embellished display font."
    },
    "world-of-water": {
        "category": "display",
        "subtype": "liquid-decorative",
        "styles": ["playful", "decorative"],
        "roles": ["display", "hero", "accent"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "droplet", "aperture": "liquid", "stroke_contrast": "fluid", "legibility_tier": "display-only"}},
        "notes": "Fluid droplet liquid-themed decorative typeface."
    },
    "relish-gargler": {
        "category": "display",
        "subtype": "heavy-psychedelic",
        "styles": ["retro", "playful", "decorative"],
        "roles": ["display", "accent"],
        "readability": {"body": 1, "long_form": 1, "ui": 1, "small_text": 1, "numbers": 3, "factors": {"x_height": "psychedelic", "aperture": "curved", "stroke_contrast": "heavy", "legibility_tier": "display-only"}},
        "notes": "Psychedelic 1970s concert poster display font."
    },
    "opsilon": {
        "category": "display",
        "subtype": "modern-geometric-display",
        "styles": ["modern", "geometric", "technical"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 3, "long_form": 2, "ui": 3, "small_text": 2, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "geometric", "stroke_contrast": "low", "legibility_tier": "display-only"}},
        "notes": "Sleek geometric display typeface."
    },
    "aclonica": {
        "category": "sans-serif",
        "subtype": "deco-rounded",
        "styles": ["modern", "playful", "art-deco"],
        "roles": ["display", "heading", "branding"],
        "readability": {"body": 5, "long_form": 4, "ui": 6, "small_text": 4, "numbers": 6, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "moderate"}},
        "notes": "Distinctive Art Deco rounded display sans."
    },
    "achtung-bravo": {
        "category": "display",
        "subtype": "decorative-headline",
        "styles": ["brutalist", "industrial", "retro"],
        "roles": ["display", "hero", "heading"],
        "readability": {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "high", "aperture": "narrow", "stroke_contrast": "none", "legibility_tier": "display-only"}},
        "notes": "Military industrial stencil headline font."
    }
}

def infer_font_intelligence(font):
    fid = font['id']
    if fid in CURATION_MAP:
        cur = dict(CURATION_MAP[fid])
        cur["fallback"] = font['curated']['fallback']
        cur["styles"] = sorted(list(set(s for s in cur.get("styles", []) if s in CONTROLLED_STYLES)))
        if not cur["styles"]:
            cur["styles"] = ["modern"]
        return cur
    
                                                              
    cur_cat = font['curated'].get('category', 'display')
    cur_sub = font['curated'].get('subtype', 'decorative-headline')
    name = font['name'].lower()
    weights = font['technical']['weights']
    
    styles = []
    roles = []
    readability = {}
    
    if cur_cat == 'sans-serif':
        styles = ["modern", "corporate"]
        if "geometric" in cur_sub: styles.append("geometric")
        if "humanist" in cur_sub: styles.append("humanist")
        if "grotesque" in cur_sub: styles.append("minimal")
        if len(weights) >= 4:
            roles = ["display", "hero", "heading", "body", "ui", "button"]
            readability = {"body": 8, "long_form": 7, "ui": 8, "small_text": 7, "numbers": 8, "factors": {"x_height": "generous", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "good"}}
        else:
            roles = ["display", "heading", "ui"]
            readability = {"body": 6, "long_form": 5, "ui": 7, "small_text": 6, "numbers": 7, "factors": {"x_height": "moderate", "aperture": "open", "stroke_contrast": "low", "legibility_tier": "moderate"}}
            
    elif cur_cat == 'serif':
        styles = ["editorial", "classic", "premium"]
        if "display" in cur_sub or "high-contrast" in cur_sub:
            styles.append("luxury")
            roles = ["display", "hero", "heading", "branding"]
            readability = {"body": 3, "long_form": 2, "ui": 2, "small_text": 1, "numbers": 6, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "high", "legibility_tier": "display-only"}}
        else:
            roles = ["heading", "body", "caption"]
            readability = {"body": 8, "long_form": 8, "ui": 6, "small_text": 6, "numbers": 7, "factors": {"x_height": "moderate", "aperture": "moderate", "stroke_contrast": "medium", "legibility_tier": "good"}}
            
    elif cur_cat == 'monospace':
        styles = ["technical", "modern"]
        roles = ["code", "number", "ui", "caption"]
        readability = {"body": 6, "long_form": 5, "ui": 7, "small_text": 6, "numbers": 9, "factors": {"x_height": "high", "aperture": "open", "stroke_contrast": "none", "legibility_tier": "optimal-code"}}
        
    elif cur_cat == 'handwriting':
        styles = ["playful", "handwritten"]
        roles = ["display", "accent", "branding"]
        readability = {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 4, "factors": {"x_height": "casual", "aperture": "open", "stroke_contrast": "variable", "legibility_tier": "accent-only"}}
        
    else:          
        styles = ["modern", "decorative"]
        if any(w in name for w in ['bold', 'chunk', 'block', 'heavy', 'black']): styles.append("brutalist")
        if any(w in name for w in ['cyber', 'future', 'techno', 'zero', 'talero', 'space']): styles.append("futuristic")
        if any(w in name for w in ['marker', 'grunge', 'street', 'graffiti', 'punk']): styles.append("grunge")
        if any(w in name for w in ['chic', 'luxury', 'deco', 'milan', 'styllo', 'paris']): styles.append("luxury")
        roles = ["display", "hero", "heading"]
        readability = {"body": 2, "long_form": 1, "ui": 2, "small_text": 1, "numbers": 5, "factors": {"x_height": "display", "aperture": "stylized", "stroke_contrast": "variable", "legibility_tier": "display-only"}}

                                
    clean_styles = sorted(list(set(s for s in styles if s in CONTROLLED_STYLES)))
    if not clean_styles:
        clean_styles = ["modern"]
        
    return {
        "category": cur_cat,
        "subtype": cur_sub,
        "styles": clean_styles,
        "roles": roles,
        "readability": readability,
        "fallback": font['curated'].get('fallback', ["sans-serif"]),
        "notes": font['curated'].get('notes')
    }

def main():
    print("Starting catalog enrichment with controlled style categories, typography roles, and readability properties...")
    
                      
    for target_dir in CATALOG_DIRS:
        schema_path = os.path.join(target_dir, "fonts.schema.json")
        fonts_path = os.path.join(target_dir, "fonts.json")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            
        curated_props = schema["properties"]["fonts"]["items"]["properties"]["curated"]
        curated_props["required"] = ["category", "subtype", "styles", "roles", "readability", "fallback"]
        
        curated_props["properties"]["styles"] = {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "enum": CONTROLLED_STYLES
            }
        }
        
        curated_props["properties"]["roles"] = {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "enum": TYPOGRAPHY_ROLES
            }
        }
        
        curated_props["properties"]["readability"] = {
            "type": "object",
            "required": ["body", "long_form", "ui", "small_text", "numbers"],
            "properties": {
                "body": {"type": "integer", "minimum": 1, "maximum": 10},
                "long_form": {"type": "integer", "minimum": 1, "maximum": 10},
                "ui": {"type": "integer", "minimum": 1, "maximum": 10},
                "small_text": {"type": "integer", "minimum": 1, "maximum": 10},
                "numbers": {"type": "integer", "minimum": 1, "maximum": 10},
                "factors": {
                    "type": "object",
                    "properties": {
                        "x_height": {"type": "string"},
                        "aperture": {"type": "string"},
                        "stroke_contrast": {"type": "string"},
                        "legibility_tier": {"type": "string"}
                    }
                }
            }
        }
        
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2)
        print(f"Updated schema at {schema_path}")
        
                              
        with open(fonts_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
            
        for font in catalog["fonts"]:
            font["curated"] = infer_font_intelligence(font)
            
                                    
        print(f"Validating catalog at {fonts_path} against updated schema...")
        jsonschema.validate(instance=catalog, schema=schema)
        print("Schema validation PASSED!")
        
        with open(fonts_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2)
        print(f"Written enriched catalog to {fonts_path} ({len(catalog['fonts'])} families)")

if __name__ == "__main__":
    main()
