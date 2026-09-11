.PHONY: install lint test api web web-test e2e screenshots

install:
	pip install -e '.[dev]'
	cd apps/web && npm install

lint:
	ruff check apps/api
	ruff format --check apps/api

format:
	ruff check --fix apps/api
	ruff format apps/api

test:
	pytest -q

api:
	uvicorn pulseforge.main:app --reload --app-dir apps/api --port 8000

web:
	cd apps/web && npm run dev

web-test:
	cd apps/web && npm test -- --run

e2e:
	cd apps/web && npm run test:e2e

screenshots:
	cd apps/web && npm run capture:screenshots
