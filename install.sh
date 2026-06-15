#!/bin/zsh
set -e

SCRIPT_DIR="${0:A:h}"
TARGET_DIR="/opt/homebrew/bin"
TARGET="$TARGET_DIR/mdtopdf"

if [[ ! -d "$TARGET_DIR" ]]; then
  TARGET_DIR="/usr/local/bin"
  TARGET="$TARGET_DIR/mdtopdf"
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "No standard local bin directory found." >&2
  exit 1
fi

chmod +x "$SCRIPT_DIR/mdtopdf" "$SCRIPT_DIR/md-to-pdf.command"
ln -sf "$SCRIPT_DIR/mdtopdf" "$TARGET"

echo "Installed: $TARGET"
echo "Usage: mdtopdf /path/to/file.md"

