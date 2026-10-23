#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo " Starting mir.ai — Realtime WebRTC Virtual Try-On Studio"
echo "=========================================================="

if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
  fi
fi

# Run with Python 3 (zero-dependency standard library server)
if command -v python3 >/dev/null 2>&1; then
  echo "Launching with Python 3..."
  exec python3 server.py
elif command -v node >/dev/null 2>&1; then
  echo "Launching with Node.js..."
  exec node server.js
else
  echo "Error: Neither python3 nor node found in PATH."
  exit 1
fi
