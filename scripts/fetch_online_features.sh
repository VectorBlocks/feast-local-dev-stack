#!/usr/bin/env bash
set -euo pipefail

docker compose exec feast-dev bash -lc "cd /workspace && python app/fetch_demo.py"
