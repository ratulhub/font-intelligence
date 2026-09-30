# Codex Instructions — Font Intelligence Thin Adapter

This workspace utilizes the **Font Intelligence Typography Decision System**.

## Canonical Source of Truth
Read and follow:
👉 [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md)

Also see root [`AGENTS.md`](AGENTS.md) for universal agent protocols.

## When to Activate
Activate Font Intelligence when:
- Writing or refactoring UI code, CSS typography, Tailwind tokens, Flutter, or React Native styling.
- Selecting, pairing, or configuring typefaces.
- Establishing typographic scales, line-heights, letter-spacing, or numerical figure alignment.
- Auditing font legibility, script coverage, or redistribution licensing.

## How to Execute
- **Recommend**: `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <web|flutter|powerpoint>`
- **Search**: `python scripts/search_fonts.py --mood "<vibe>" --role <body> --min-readability 8`
- **Score Pair**: `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`
- **Export & Prune**: `python scripts/copy_fonts.py --fonts "<id1,id2>" --dest "<path>" --prune-unused`
- **Clean User Project**: `python scripts/clean_project.py --project-dir <path>`
- **Offline / Direct Catalog Reading**: Read `catalog/fonts.json`, `catalog/use-cases.json`, and `catalog/pairings.json`.
- **Compact Fallback**: Use [`lite/font-intelligence-lite.md`](lite/font-intelligence-lite.md).

## Non-Negotiable Hard Rules
1. Never invent fonts, weights, or language scripts.
2. Never assign decorative or display typefaces to body/UI text.
3. Respect explicit user font preferences (anchor and pair around them).
4. Maximum 2 primary families (heading + body) + monospace only when code/data is present.
5. Zero-bloat delivery: leave only used font files in user projects; prune unneeded fonts and remove temporary skill folders upon completion.
6. Refer to [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md) for the full 10-step workflow.
