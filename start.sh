#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
cd "$SCRIPT_DIR/backend"
python app_telegram.py
