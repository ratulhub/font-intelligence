# Font Intelligence: Thin Platform Adapters

This directory stores reference configurations and thin platform adapters for modern coding agents and AI IDEs.

## Architecture: Single Canonical Truth

All coding agents share a single core skill, identical catalog, and unified rules:
```
CORE SKILL (.agents/skills/font-intelligence/SKILL.md)
  ├── Thin Adapters (Pointers only; never duplicate the skill):
  │   ├── Antigravity   → .agents/skills/font-intelligence/ & .agents/rules/font-intelligence.md
  │   ├── Claude Code   → CLAUDE.md
  │   ├── Codex         → AGENTS.md & .codex/instructions.md
  │   ├── Cursor        → .cursorrules & .cursor/rules/font-intelligence.mdc
  │   ├── Windsurf      → .windsurfrules
  │   ├── Cline         → .clinerules
  │   ├── GitHub Copilot→ .github/copilot-instructions.md
  │   └── Gemini CLI    → GEMINI.md
  ├── Compact Fallback  → lite/font-intelligence-lite.md
  └── Canonical Data    → catalog/ (fonts, use-cases, pairings, scoring, anti-patterns)
```

## Available Adapters

| Platform | Configuration File | Purpose |
| :--- | :--- | :--- |
| **Antigravity** | `.agents/skills/font-intelligence/SKILL.md` | Core canonical skill |
| **Claude Code** | `CLAUDE.md` | Claude Code CLI project instructions |
| **Cursor** | `.cursor/rules/font-intelligence.mdc` & `.cursorrules` | Cursor IDE rules (MDC format) |
| **Windsurf** | `.windsurfrules` | Windsurf Cascade rules |
| **Cline** | `.clinerules` | Cline extension rules |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Copilot Workspace instructions |
| **Codex** | `.codex/instructions.md` | OpenAI Codex instructions |
| **Gemini CLI** | `GEMINI.md` | Gemini CLI Thin Adapter |

## Automated Installation

To install or configure adapters in a target project or global config:
```bash
# Bash (macOS / Linux)
./install.sh all
./install.sh cursor
./install.sh claude --global

# PowerShell (Windows)
.\install.ps1 -Target all
.\install.ps1 -Target cursor
.\install.ps1 -Target antigravity -Global
```
