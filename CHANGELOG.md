# Changelog

All notable changes to the **Font Intelligence Typography Decision System** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-09-29

### Added
- **Core Skill & Architecture**:
  - Canonical typography decision skill at [`.agents/skills/font-intelligence/SKILL.md`](file:///d:/font-intelligence/.agents/skills/font-intelligence/SKILL.md).
  - Multi-agent thin adapter architecture supporting Antigravity, Claude Code, Cursor, Windsurf, Cline, GitHub Copilot, Codex, and Gemini CLI.
  - Compact fallback cheatsheet at [`lite/font-intelligence-lite.md`](file:///d:/font-intelligence/lite/font-intelligence-lite.md) for constrained context windows and offline LLMs.
- **Font Catalog & Data Foundation**:
  - `catalog/fonts.json`: 103 verified font families, 475 font binary files, with verified OpenType tables, weights, styles, variable axes, Unicode blocks, and calibrated readability metrics (1–10).
  - `catalog/use-cases.json`: 29 project situations across Web, Mobile (Flutter, React Native), and Documents (PowerPoint, Word, PDF). Includes style vibe interpretation dictionary.
  - `catalog/pairings.json`: 12 masterclass curated pairings with deep typographic rationales and optical contrast metrics.
  - `catalog/scoring.json`: 10-dimensional mathematical pairing scoring engine with weighted dimensions.
  - `catalog/anti-patterns.json`: 10 lethal typography anti-patterns with severity penalties (-15 to -45 points).
- **Supporting Python CLI Tools**:
  - `scripts/scan_fonts.py`: High-speed OpenType parser extracting TrueType/OpenType metadata and Unicode blocks.
  - `scripts/build_catalog.py`: Safe, deterministic catalog compiler preserving curated editorial fields.
  - `scripts/search_fonts.py`: Multi-criteria search CLI by mood, role, minimum readability, and script.
  - `scripts/recommend.py`: Project brief recommender accepting free-text briefs, CLI flags, user anchors, and existing fonts.
  - `scripts/score_pair.py`: Comprehensive 10-dimensional pair evaluation and anti-pattern diagnostic.
  - `scripts/copy_fonts.py`: Safe asset export tool with format filtering, license bundling, and code generation.
  - `scripts/validate_catalog.py`: Deep schema, file path, ID uniqueness, and broken reference validator.
  - `scripts/validate_licenses.py`: Legal redistribution and commercial permission audit tool.
- **Visual Inspection System**:
  - `preview/index.html`: Interactive typography preview studio with dynamic filtering by category, style, role, script, and readability.
  - Interactive type tester with live editable samples for Latin, numbers, UI controls, and non-Latin scripts.
- **Licensing & Documentation**:
  - `docs/redistribution-review.md`: Exhaustive redistribution audit covering all 103 families with SPDX licenses and commercial proof requirements.
  - `docs/evaluation-report.md`: Real-user evaluation report testing 16 project briefs and 8 adversarial edge cases.
  - `.github/workflows/validate.yml`: Continuous Integration workflow running catalog, licensing, and engine validation on Python 3.10–3.12.

### Fixed
- **Secondary Weight Fallback**: Resolved a bug in `evaluate_pairing()` where `p_weights[0]` was erroneously accessed instead of `s_weights[0]`, preventing single-weight fonts from hallucinating light weights.
- **Readability Rationale Accuracy**: Added dynamic threshold check in `_generate_explanation()` to prevent low-readability body fonts from falsely claiming "robust legibility".
- **Companion Font Fallback Injection**: Injected verified non-Latin companion fonts (`Hind Siliguri`, `Noto Sans Bengali`) directly into CSS custom properties and Flutter/React Native fallback stacks.
- **Catalog Alias Collision**: Corrected alias definitions for `ubuntu-mono` and `ubuntu-condensed` in `catalog/fonts.json`, and added strict ID-first precedence in `TypographyEngine` font indexing.
- **User Preference Anchoring**: Added `--anchor` and `--existing-fonts` parameters to `recommend.py` to strictly enforce Hard Rules 5 & 6.
- **Asset Export License Warnings**: Added prominent warning banners in `copy_fonts.py` when exporting fonts with `UNKNOWN`, `RESTRICTED`, or `PROOF_NEEDED` status.
