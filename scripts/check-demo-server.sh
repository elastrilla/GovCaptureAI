#!/usr/bin/env sh
set -eu

DEMO_HOST="${1:-${DEMO_HOST:-192.168.1.51}}"
EXPECTED_FRONTEND_VERSION="${EXPECTED_FRONTEND_VERSION:-13c-company-award}"

check_url() {
  label="$1"
  url="$2"

  if curl -fsS "$url" >/dev/null; then
    echo "${label}: OK (${url})"
  else
    echo "${label}: NOT READY (${url})"
    return 1
  fi
}

check_url "Backend health" "http://${DEMO_HOST}:8000/health"
check_url "Frontend dashboard" "http://${DEMO_HOST}:8001"

if curl -fsS "http://${DEMO_HOST}:8001/index.html" | grep -q "${EXPECTED_FRONTEND_VERSION}"; then
  echo "Frontend version: OK (${EXPECTED_FRONTEND_VERSION})"
else
  echo "Frontend version: OUTDATED or unreadable (expected ${EXPECTED_FRONTEND_VERSION})"
  echo "Run ./scripts/sync-to-pi.sh and ./scripts/deploy-pi.sh, then check again."
  exit 1
fi
