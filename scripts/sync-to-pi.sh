#!/usr/bin/env sh
set -eu

PI_HOST="${PI_HOST:-192.168.1.51}"
PI_USER="${PI_USER:-elastrilla}"
PI_PATH="${PI_PATH:-~/GovCaptureAI}"

rsync -av \
  --exclude backend/venv \
  --exclude backend/.env \
  --exclude .git \
  --exclude .codex_tmp \
  --exclude outputs \
  --exclude __pycache__ \
  --exclude '*.pyc' \
  --exclude '.DS_Store' \
  ./ "${PI_USER}@${PI_HOST}:${PI_PATH}/"

echo "Synced GovCaptureAI to ${PI_USER}@${PI_HOST}:${PI_PATH}"
