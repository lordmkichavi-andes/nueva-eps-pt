.PHONY: up down test-api test-web build-web

up:
	docker compose up -d --build

down:
	docker compose down

test-api:
	cd eps-solicitudes-api && \
	  (test -d .venv || python3 -m venv .venv) && \
	  .venv/bin/python -m pip install -q -r requirements-dev.txt && \
	  .venv/bin/python -m pytest -v

test-web:
	cd eps-solicitudes-web && 	npx ng test --no-watch --browsers=ChromeHeadless

build-web:
	cd eps-solicitudes-web && npm ci && npm run build
