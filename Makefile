.PHONY: install dev lint format typecheck test migrate docker-up docker-down clean

install:
	pip install -r requirements-dev.txt

dev:
	uvicorn app.main:app --reload

lint:
	ruff check app/ tests/

format:
	ruff format app/ tests/

typecheck:
	mypy app/

test:
	pytest tests/ -v --asyncio-mode=auto --cov=app -x

migrate:
	alembic upgrade head

docker-up:
	docker compose up -d

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov *.db
