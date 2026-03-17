SHELL := /bin/bash
CONTAINER := feast-dev
REPO_DIR := /workspace/example_repo

up:
	docker compose up -d --build

down:
	docker compose down -v

shell:
	docker compose exec $(CONTAINER) bash

apply:
	docker compose exec $(CONTAINER) bash -lc "cd $(REPO_DIR) && python generate_sample_data.py && feast apply"

materialize:
	docker compose exec $(CONTAINER) bash -lc "cd $(REPO_DIR) && python generate_sample_data.py && feast materialize-incremental $$(date -u +%Y-%m-%dT%H:%M:%S)"

fetch:
	docker compose exec $(CONTAINER) bash -lc "cd /workspace && python app/fetch_demo.py"

ui:
	docker compose exec $(CONTAINER) bash -lc "cd $(REPO_DIR) && feast ui -h 0.0.0.0 -p 8888"

notebook:
	docker compose exec -e JUPYTER_CONFIG_DIR=/workspace/.jupyter $(CONTAINER) bash -lc "cd /workspace && jupyter lab --ip=0.0.0.0 --port=8889 --no-browser --allow-root --ServerApp.token='' --ServerApp.password=''"

bootstrap:
	docker compose exec $(CONTAINER) bash -lc "cd /workspace/example_repo && python generate_sample_data.py && feast apply"
