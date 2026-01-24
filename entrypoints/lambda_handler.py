"""
AWS Lambda entrypoint using Mangum adapter.
This wraps the FastAPI app for Lambda deployment.
"""
from mangum import Mangum
from src.presentation.api.app import create_app

app = create_app()
handler = Mangum(app, lifespan="off")
