#!/usr/bin/env bash
set -euo pipefail

TS=$(date -u +%Y-%m-%dT%H:%M:%S)
docker compose exec feast-dev bash -lc "cd /workspace/example_repo && python generate_sample_data.py && feast materialize-incremental ${TS}"
