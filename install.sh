#!/usr/bin/env bash
set -e

# Claude Essential Mode Installer for macOS / Linux / WSL

CLAUDE_DIR="$HOME/.claude"
STYLES_DIR="$CLAUDE_DIR/output-styles"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
TARGET_FILE="$STYLES_DIR/essential.md"
SOURCE_URL="https://raw.githubusercontent.com/Iliesseu28/claude-essential-mode/main/styles/essential.md"

echo "Installing Essential Mode for Claude Code..."

mkdir -p "$STYLES_DIR"

if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$SOURCE_URL" -o "$TARGET_FILE"
elif command -v wget >/dev/null 2>&1; then
    wget -qO "$TARGET_FILE" "$SOURCE_URL"
else
    echo "Error: curl or wget is required." >&2
    exit 1
fi

# Update settings.json if jq or python3 is available
if [ -f "$SETTINGS_FILE" ]; then
    if command -v python3 >/dev/null 2>&1; then
        python3 - <<EOF
import json
try:
    with open("$SETTINGS_FILE", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    data = {}
data["outputStyle"] = "Essential"
with open("$SETTINGS_FILE", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
EOF
        echo "Updated $SETTINGS_FILE with outputStyle: 'Essential'"
    fi
fi

echo "Successfully installed Essential Mode!"
echo "Claude Code will now respond in Essential Mode by default."
echo "To switch manually anytime in a session: /output-style essential"
