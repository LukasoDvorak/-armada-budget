#!/bin/bash
# Armada Budget — local dev server
# Double-click in Finder to start

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 not found" message "Install Python 3 from python.org"'
    exit 1
fi

echo "Starting Armada Budget local server..."
python3 armada_local.py
