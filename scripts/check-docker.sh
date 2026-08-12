#!/usr/bin/env sh
set -eu

docker_version="$(docker --version 2>/dev/null || true)"
compose_v2="$(docker compose version 2>/dev/null || true)"
compose_v1="$(docker-compose --version 2>/dev/null || true)"

if [ -z "$docker_version" ]; then
  echo "Docker is not available. Install Docker Desktop before running the demo stack."
  exit 1
fi

echo "$docker_version"

if [ -n "$compose_v2" ]; then
  echo "$compose_v2"
elif [ -n "$compose_v1" ]; then
  echo "$compose_v1"
else
  echo "Docker Compose is not available. Install Docker Desktop with Compose support."
  exit 1
fi

major_version="$(echo "$docker_version" | sed -n 's/^Docker version \([0-9][0-9]*\).*/\1/p')"

if [ -n "$major_version" ] && [ "$major_version" -lt 20 ]; then
  echo "Docker is older than the supported demo baseline."
  echo "Please update Docker Desktop, then rerun: docker-compose up --build"
  exit 1
fi

echo "Docker preflight passed."
