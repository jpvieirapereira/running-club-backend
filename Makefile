.PHONY: help install dev run test clean docker-up docker-down

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with UV
	uv pip install -r pyproject.toml

dev: ## Install dev dependencies
	uv pip install -r pyproject.toml --extra dev

run: ## Run the application locally
	uvicorn entrypoints.asgi:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest tests/ -v

docker-up: ## Start all services with Docker Compose
	docker-compose up --build

docker-down: ## Stop all Docker services
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

clean: ## Clean up cache and build files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/

localstack: ## Start only LocalStack
	docker-compose up localstack

setup: ## Initial setup (copy .env, install deps)
	@if [ ! -f .env ]; then cp .env.example .env; echo ".env created"; fi
	uv pip install -r pyproject.toml
	@echo "Setup complete! Run 'make docker-up' to start"
