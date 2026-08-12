#!/usr/bin/env sh
set -eu

PI_HOST="${PI_HOST:-192.168.1.51}"
PI_USER="${PI_USER:-elastrilla}"
PI_PATH="${PI_PATH:-~/GovCaptureAI}"

ssh "${PI_USER}@${PI_HOST}" "
  set -eu
  cd ${PI_PATH}
  ./scripts/check-docker.sh
  docker-compose up --build -d
  docker-compose ps
"

echo "GovCaptureAI demo requested on ${PI_HOST}."
echo "Dashboard:   http://${PI_HOST}:8001"
echo "Backend API: http://${PI_HOST}:8000/docs"
