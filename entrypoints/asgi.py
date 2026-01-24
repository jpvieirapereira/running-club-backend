"""
ASGI entrypoint for local development and container deployment.
Run with: uvicorn entrypoints.asgi:app --reload
"""
from src.presentation.api.app import create_app

app = create_app()
