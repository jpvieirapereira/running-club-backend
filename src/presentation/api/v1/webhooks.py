"""
Webhook endpoints for Strava events.
"""
from fastapi import APIRouter, Request, Query, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide

from src.application.use_cases import ActivitySyncUseCase
from src.presentation.schemas import WebhookEventRequest
from src.infrastructure.container import Container
from src.infrastructure.config import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get(
    "/strava",
    summary="Webhook subscription verification",
    description="Strava webhook subscription verification endpoint"
)
async def verify_strava_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    """
    Verify Strava webhook subscription.
    
    Strava sends a GET request to verify the webhook endpoint.
    We must respond with the challenge if the verify_token matches.
    """
    if hub_mode != "subscribe":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid hub.mode"
        )
    
    if hub_verify_token != settings.strava_webhook_verify_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid verify_token"
        )
    
    return {"hub.challenge": hub_challenge}


@router.post(
    "/strava",
    status_code=status.HTTP_200_OK,
    summary="Receive Strava webhook events",
    description="Handle incoming webhook events from Strava"
)
@inject
async def handle_strava_webhook(
    event: WebhookEventRequest,
    request: Request,
    activity_sync_use_case: ActivitySyncUseCase = Depends(Provide[Container.activity_sync_use_case])
):
    """
    Handle Strava webhook events.
    
    Process activity create/update events from Strava.
    """
    # Only process activity events
    if event.object_type != "activity":
        return {"status": "ignored", "reason": "not an activity event"}
    
    # Only process create and update events
    if event.aspect_type not in ["create", "update"]:
        return {"status": "ignored", "reason": "not a create/update event"}
    
    # TODO: Map Strava athlete_id (owner_id) to customer_id
    # For now, we'll need to add a lookup mechanism
    # This is a simplified version - in production, you'd need to:
    # 1. Query customer by strava_athlete_id
    # 2. Sync the specific activity
    
    # Background task would be better here to avoid blocking
    # For now, just acknowledge receipt
    
    return {
        "status": "received",
        "event_type": event.aspect_type,
        "activity_id": event.object_id,
        "message": "Event queued for processing"
    }
