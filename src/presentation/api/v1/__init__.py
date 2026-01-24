from fastapi import APIRouter
from src.presentation.api.v1 import auth, public, training_plans, strava, webhooks

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(public.router)
api_router.include_router(training_plans.router)
api_router.include_router(strava.router)
api_router.include_router(webhooks.router)
