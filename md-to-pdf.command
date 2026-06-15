#!/bin/zsh
SCRIPT_DIR="${0:A:h}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/TeX/texbin:/opt/anaconda3/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
PYTHON_BIN="$(command -v python3)"

if [[ -z "$PYTHON_BIN" ]]; then
  osascript -e 'display dialog "python3 was not found." buttons {"OK"} default button "OK"'
  exit 1
fi

cd "$SCRIPT_DIR"
"$PYTHON_BIN" "$SCRIPT_DIR/md_to_pdf_converter.py"

