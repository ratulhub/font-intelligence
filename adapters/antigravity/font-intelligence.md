# Antigravity Workspace Rule: Font Intelligence

Activate the **Font Intelligence Typography Decision System** whenever a user task touches font selection, typography hierarchy, UI styling, CSS font stacks, or visual design tokens.

## Canonical Skill
Invoke the canonical skill instructions:
👉 [`.agents/skills/font-intelligence/SKILL.md`](file:///d:/font-intelligence/.agents/skills/font-intelligence/SKILL.md)

## Rapid Execution
- Run `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <plat>` for data-backed recommendations.
- Score pairings with `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`.
- If offline, parse `catalog/use-cases.json` and `catalog/fonts.json` directly.
- For quick reference, check [`lite/font-intelligence-lite.md`](file:///d:/font-intelligence/lite/font-intelligence-lite.md).

## Hard Constraints
- Never default to generic popular fonts (Inter, Roboto, Arial) without explicit project justification.
- Never invent fonts, weights, or script coverage.
- Strictly enforce `body` readability $\ge 7/10$.
- Respect user-specified fonts as primary anchors.
