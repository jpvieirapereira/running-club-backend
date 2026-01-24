"""
Strava integration API endpoints.
"""
from typing import List, Union
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from dependency_injector.wiring import inject, Provide

from src.application.use_cases import StravaIntegrationUseCase, ActivitySyncUseCase
from src.application.dtos import CoachDTO, CustomerDTO
from src.presentation.api.dependencies import get_current_active_user
from src.presentation.schemas import (
    StravaConnectionResponse,
    StravaAuthCallbackRequest,
    ActivitySummaryResponse,
    ActivityDetailResponse,
    ActivityFilterRequest,
    ActivitySyncResponse
)
from src.infrastructure.container import Container
from src.infrastructure.config import settings

router = APIRouter(prefix="/strava", tags=["strava"])


@router.get(
    "/connect",
    response_model=dict,
    summary="Get Strava authorization URL",
    description="Get OAuth authorization URL for connecting Strava account"
)
@inject
async def get_strava_connect_url(
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    strava_use_case: StravaIntegrationUseCase = Depends(Provide[Container.strava_integration_use_case])
):
    """
    Get Strava OAuth authorization URL.
    
    Only customers can connect Strava accounts.
    """
    if not isinstance(current_user, CustomerDTO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can connect Strava accounts"
        )
    
    auth_url = await strava_use_case.get_authorization_url(
        customer_id=current_user.id,
        redirect_uri=settings.strava_callback_url
    )
    
    return {
        "authorization_url": auth_url,
        "instructions": "Visit this URL to authorize Strava access"
    }


@router.get(
    "/callback",
    response_model=StravaConnectionResponse,
    summary="OAuth callback endpoint",
    description="Handle Strava OAuth callback and exchange code for tokens"
)
@inject
async def strava_callback(
    code: str = Query(..., description="Authorization code from Strava"),
    scope: str = Query(..., description="Granted scopes"),
    state: str = Query(None, description="State parameter"),
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    strava_use_case: StravaIntegrationUseCase = Depends(Provide[Container.strava_integration_use_case])
):
    """
    Handle Strava OAuth callback.
    
    Exchange authorization code for access token and connect account.
    """
    if not isinstance(current_user, CustomerDTO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can connect Strava accounts"
        )
    
    try:
        connection = await strava_use_case.exchange_code(
            code=code,
            customer_id=current_user.id
        )
        
        return StravaConnectionResponse(
            is_connected=True,
            athlete_id=connection.athlete_id,
            connected_at=connection.connected_at,
            last_sync_at=connection.last_sync_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to connect Strava: {str(e)}"
        )


@router.delete(
    "/disconnect",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Disconnect Strava account",
    description="Revoke Strava access and disconnect account"
)
@inject
async def disconnect_strava(
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    strava_use_case: StravaIntegrationUseCase = Depends(Provide[Container.strava_integration_use_case])
):
    """Disconnect Strava account."""
    if not isinstance(current_user, CustomerDTO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can disconnect Strava accounts"
        )
    
    await strava_use_case.disconnect(current_user.id)


@router.get(
    "/status",
    response_model=StravaConnectionResponse,
    summary="Get Strava connection status",
    description="Check if customer's Strava account is connected"
)
@inject
async def get_strava_status(
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    strava_use_case: StravaIntegrationUseCase = Depends(Provide[Container.strava_integration_use_case])
):
    """Get Strava connection status."""
    if not isinstance(current_user, CustomerDTO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can check Strava status"
        )
    
    connection = await strava_use_case.get_connection_status(current_user.id)
    
    if not connection:
        return StravaConnectionResponse(is_connected=False)
    
    return StravaConnectionResponse(
        is_connected=True,
        athlete_id=connection.athlete_id,
        connected_at=connection.connected_at,
        last_sync_at=connection.last_sync_at
    )


@router.post(
    "/sync",
    response_model=ActivitySyncResponse,
    summary="Manually sync Strava activities",
    description="Trigger manual sync of activities from Strava"
)
@inject
async def sync_strava_activities(
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    activity_sync_use_case: ActivitySyncUseCase = Depends(Provide[Container.activity_sync_use_case])
):
    """Manually sync Strava activities."""
    if not isinstance(current_user, CustomerDTO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can sync activities"
        )
    
    try:
        result = await activity_sync_use_case.sync_activities(current_user.id)
        
        return ActivitySyncResponse(
            synced_count=result.synced_count,
            matched_count=result.matched_count,
            error_count=result.error_count,
            message=f"Successfully synced {result.synced_count} activities, matched {result.matched_count} to training days"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/activities",
    response_model=List[ActivitySummaryResponse],
    summary="List customer's Strava activities",
    description="Get list of synced Strava activities with optional filters"
)
@inject
async def list_strava_activities(
    start_date: str = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    match_status: str = Query(None, description="Filter by match status"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    activity_sync_use_case: ActivitySyncUseCase = Depends(Provide[Container.activity_sync_use_case])
):
    """List customer's Strava activities."""
    if not isinstance(current_user, CustomerDTO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can view their activities"
        )
    
    from datetime import date as date_type
    from src.domain.entities.enums import ActivityMatchStatus
    
    # Parse filters
    start = date_type.fromisoformat(start_date) if start_date else None
    end = date_type.fromisoformat(end_date) if end_date else None
    status_filter = ActivityMatchStatus(match_status) if match_status else None
    
    activities = await activity_sync_use_case.get_customer_activities(
        customer_id=current_user.id,
        start_date=start,
        end_date=end,
        match_status=status_filter,
        limit=limit
    )
    
    return [
        ActivitySummaryResponse(
            id=a.id,
            strava_activity_id=a.strava_activity_id,
            name=a.name,
            activity_type=a.activity_type,
            start_date=a.start_date,
            distance=a.distance,
            moving_time=a.moving_time,
            pace_min_per_km=a.average_pace,
            elevation_gain=a.total_elevation_gain,
            matched=a.match_status.value == "matched",
            training_day_id=a.training_day_id
        )
        for a in activities
    ]


@router.get(
    "/activities/{activity_id}",
    response_model=ActivityDetailResponse,
    summary="Get activity detail",
    description="Get detailed information about a specific activity"
)
@inject
async def get_activity_detail(
    activity_id: UUID,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    activity_sync_use_case: ActivitySyncUseCase = Depends(Provide[Container.activity_sync_use_case])
):
    """Get detailed activity information."""
    user_type = "customer" if isinstance(current_user, CustomerDTO) else "coach"
    
    activity = await activity_sync_use_case.get_activity_by_id(
        activity_id=activity_id,
        requesting_user_id=current_user.id,
        requesting_user_type=user_type
    )
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return ActivityDetailResponse(**activity.__dict__)
