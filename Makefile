# Atajos desde la raíz del repo (requiere `make`; opcional).
.PHONY: up down test-api test-web build-web

up:
	docker compose up -d --build

down:
	docker compose down

# API: crea .venv si no existe, instala deps y ejecuta pytest
test-api:
	cd eps-solicitudes-api && \
	  (test -d .venv || python3 -m venv .venv) && \
	  .venv/bin/python -m pip install -q -r requirements-dev.txt && \
	  .venv/bin/python -m pytest -v

# Front: tests en Chrome headless (requiere npm install previo)
test-web:
	cd eps-solicitudes-web && npx ng test --no-watch --browsers=ChromeHeadless

# Front: solo compila (útil en CI o sin Chrome)
build-web:
	cd eps-solicitudes-web && npm ci && npm run build
