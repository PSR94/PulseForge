PYTHON ?= python
NPM ?= npm

.PHONY: install dev up down test backend-test frontend-test lint backend-lint frontend-lint e2e migrate doctor screenshots observability clean

install:
	$(PYTHON) -m pip install -e ".[dev]"
	cd apps/web && $(NPM) install

dev:
	docker compose up --build

up:
	docker compose up --build -d

down:
	docker compose down

test: backend-test frontend-test

backend-test:
	pytest apps/api/tests -q

frontend-test:
	cd apps/web && $(NPM) test

lint: backend-lint frontend-lint

backend-lint:
	ruff check apps/api
	$(PYTHON) -m compileall -q apps/api/pulseforge

frontend-lint:
	cd apps/web && $(NPM) run lint

e2e:
	cd apps/web && npx playwright test

migrate:
	alembic upgrade head

doctor:
	$(PYTHON) scripts/doctor.py

screenshots:
	mkdir -p docs/images
	cd apps/web && npx playwright test e2e/screenshots.spec.ts --project=chromium

observability:
	docker compose --profile observability up --build

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	rm -rf apps/web/.next apps/web/node_modules/.cache apps/web/playwright-report apps/web/test-results
