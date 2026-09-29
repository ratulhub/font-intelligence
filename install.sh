#!/usr/bin/env bash
# ==============================================================================
# Font Intelligence - Unified Multi-Agent Installer (Bash)
# Installs Font Intelligence skill and platform adapters deterministically.
# Usage:
#   ./install.sh [all|antigravity|claude|cursor|windsurf|cline|copilot|codex|gemini] [--global]
# ==============================================================================

set -euo pipefail

TARGET="${1:-all}"
IS_GLOBAL=false
DEST_DIR=""

for arg in "$@"; do
    case "$arg" in
        --global) IS_GLOBAL=true ;;
        --dest=*) DEST_DIR="${arg#*=}" ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -z "$DEST_DIR" ]; then
    DEST_DIR="$SCRIPT_DIR"
fi

echo "================================================================="
echo "Installing Font Intelligence Typography Decision System"
echo "Target Adapter: $TARGET (Global: $IS_GLOBAL)"
echo "Source Path:    $SCRIPT_DIR"
echo "Destination:    $DEST_DIR"
echo "================================================================="

copy_safe() {
    local src="$1"
    local dest="$2"
    if [ "$src" != "$dest" ]; then
        mkdir -p "$(dirname "$dest")"
        cp -f "$src" "$dest"
    fi
}

install_antigravity() {
    echo "• Configuring Antigravity..."
    local dest
    if [ "$IS_GLOBAL" = true ]; then
        dest="$HOME/.gemini/config/skills/font-intelligence"
    else
        dest="$DEST_DIR/.agents/skills/font-intelligence"
    fi
    mkdir -p "$dest"
    if [ "$SCRIPT_DIR/.agents/skills/font-intelligence" != "$dest" ]; then
        cp -rf "$SCRIPT_DIR/.agents/skills/font-intelligence/"* "$dest/"
    fi
    echo "  -> Antigravity skill ready at: $dest"
}

install_claude() {
    echo "• Configuring Claude Code..."
    local dest
    if [ "$IS_GLOBAL" = true ]; then
        dest="$HOME/.claude/CLAUDE.md"
    else
        dest="$DEST_DIR/CLAUDE.md"
    fi
    copy_safe "$SCRIPT_DIR/adapters/claude/CLAUDE.md" "$dest"
    echo "  -> Claude adapter ready at: $dest"
}

install_cursor() {
    echo "• Configuring Cursor..."
    local rules_dir="$DEST_DIR/.cursor/rules"
    copy_safe "$SCRIPT_DIR/adapters/cursor/font-intelligence.mdc" "$rules_dir/font-intelligence.mdc"
    copy_safe "$SCRIPT_DIR/adapters/cursor/.cursorrules" "$DEST_DIR/.cursorrules"
    echo "  -> Cursor rules ready at: $rules_dir/font-intelligence.mdc"
}

install_windsurf() {
    echo "• Configuring Windsurf..."
    copy_safe "$SCRIPT_DIR/adapters/windsurf/.windsurfrules" "$DEST_DIR/.windsurfrules"
    echo "  -> Windsurf rule ready at: $DEST_DIR/.windsurfrules"
}

install_cline() {
    echo "• Configuring Cline..."
    copy_safe "$SCRIPT_DIR/adapters/cline/.clinerules" "$DEST_DIR/.clinerules"
    echo "  -> Cline rule ready at: $DEST_DIR/.clinerules"
}

install_copilot() {
    echo "• Configuring GitHub Copilot..."
    local dest="$DEST_DIR/.github/copilot-instructions.md"
    copy_safe "$SCRIPT_DIR/adapters/copilot/copilot-instructions.md" "$dest"
    echo "  -> Copilot instructions ready at: $dest"
}

install_codex() {
    echo "• Configuring Codex..."
    local dest="$DEST_DIR/.codex/instructions.md"
    copy_safe "$SCRIPT_DIR/adapters/codex/instructions.md" "$dest"
    echo "  -> Codex instructions ready at: $dest"
}

install_gemini() {
    echo "• Configuring Gemini CLI..."
    copy_safe "$SCRIPT_DIR/adapters/gemini/GEMINI.md" "$DEST_DIR/GEMINI.md"
    echo "  -> Gemini CLI adapter ready at: $DEST_DIR/GEMINI.md"
}

case "$TARGET" in
    antigravity) install_antigravity ;;
    claude)      install_claude ;;
    cursor)      install_cursor ;;
    windsurf)    install_windsurf ;;
    cline)       install_cline ;;
    copilot)     install_copilot ;;
    codex)       install_codex ;;
    gemini)      install_gemini ;;
    all)
        install_antigravity
        install_claude
        install_cursor
        install_windsurf
        install_cline
        install_copilot
        install_codex
        install_gemini
        ;;
    *)
        echo "Unknown target: $TARGET"
        echo "Supported: all, antigravity, claude, cursor, windsurf, cline, copilot, codex, gemini"
        exit 1
        ;;
esac

echo ""
echo "Running post-install catalog validation..."
if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/scripts/validate_catalog.py"
elif command -v python &>/dev/null; then
    python "$SCRIPT_DIR/scripts/validate_catalog.py"
fi

echo "================================================================="
echo "Font Intelligence installation completed successfully!"
echo "================================================================="
