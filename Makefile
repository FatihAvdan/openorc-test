.PHONY: install dev lint test docker-up docker-down clean

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

lint:
	ruff check app/ tests/

test:
	pytest tests/ -v --asyncio-mode=auto

docker-up:
	docker compose up -d

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache
