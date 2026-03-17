#!/usr/bin/env bash
set -euo pipefail

docker compose up -d --build
sleep 3
docker compose exec feast-dev bash -lc "cd /workspace/example_repo && python generate_sample_data.py && feast apply"

echo "Bootstrap complete."
