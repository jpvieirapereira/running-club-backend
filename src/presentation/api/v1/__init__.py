from fastapi import APIRouter
from src.presentation.api.v1 import auth, tasks

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
