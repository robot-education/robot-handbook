#!/bin/bash
# A trivial wrapper for build.py
source .venv/bin/activate
exec "python" "-m" "build" "$@"
