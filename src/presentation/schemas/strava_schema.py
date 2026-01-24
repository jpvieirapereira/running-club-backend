"""
Strava activity Pydantic schemas.
"""
from datetime import datetime, date
from typing import Optional, Dict, List, Any
from uuid import UUID
from pydantic import BaseModel, Field

from src.domain.entities.enums import ActivityMatchStatus


class StravaConnectionResponse(BaseModel):
    """Response for Strava connection status."""
    is_connected: bool
    athlete_id: Optional[int] = None
    connected_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_connected": True,
                "athlete_id": 12345678,
                "connected_at": "2024-01-20T10:30:00",
                "last_sync_at": "2024-01-24T11:00:00"
            }
        }


class StravaAuthCallbackRequest(BaseModel):
    """Request from Strava OAuth callback."""
    code: str
    scope: str
    state: Optional[str] = None


class ActivitySummaryResponse(BaseModel):
    """Summary response for list views."""
    id: UUID
    strava_activity_id: int
    name: str
    activity_type: str
    start_date: datetime
    distance: float = Field(..., description="Distance in meters")
    moving_time: int = Field(..., description="Moving time in seconds")
    pace_min_per_km: Optional[float] = Field(None, description="Average pace in min/km")
    elevation_gain: Optional[float] = Field(None, description="Elevation gain in meters")
    matched: bool = Field(..., description="Whether activity is matched to training day")
    training_day_id: Optional[UUID] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "strava_activity_id": 12345678901,
                "name": "Morning Run",
                "activity_type": "Run",
                "start_date": "2024-01-24T07:30:00",
                "distance": 8000,
                "moving_time": 2400,
                "pace_min_per_km": 5.0,
                "elevation_gain": 150,
                "matched": True,
                "training_day_id": "660e8400-e29b-41d4-a716-446655440001"
            }
        }


class ActivityDetailResponse(BaseModel):
    """Detailed activity response."""
    id: UUID
    customer_id: UUID
    strava_activity_id: int
    name: str
    activity_type: str
    start_date: datetime
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: Optional[float] = None
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    average_pace: Optional[float] = None
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    heartrate_zones: Optional[Dict[str, Any]] = None
    splits: Optional[List[Dict[str, Any]]] = None
    laps: Optional[List[Dict[str, Any]]] = None
    calories: Optional[float] = None
    suffer_score: Optional[float] = None
    kudos_count: int = 0
    comment_count: int = 0
    achievement_count: int = 0
    photos: Optional[List[str]] = None
    map_polyline: Optional[str] = None
    training_day_id: Optional[UUID] = None
    match_status: ActivityMatchStatus
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "customer_id": "440e8400-e29b-41d4-a716-446655440000",
                "strava_activity_id": 12345678901,
                "name": "Morning Run",
                "activity_type": "Run",
                "start_date": "2024-01-24T07:30:00",
                "distance": 8000,
                "moving_time": 2400,
                "elapsed_time": 2500,
                "total_elevation_gain": 150,
                "average_speed": 3.33,
                "average_heartrate": 145,
                "max_heartrate": 165,
                "kudos_count": 5,
                "match_status": "matched",
                "training_day_id": "660e8400-e29b-41d4-a716-446655440001",
                "created_at": "2024-01-24T08:00:00"
            }
        }


class ActivityFilterRequest(BaseModel):
    """Filter options for activity list."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    match_status: Optional[ActivityMatchStatus] = None
    limit: int = Field(default=50, ge=1, le=200)
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "match_status": "matched",
                "limit": 50
            }
        }


class ActivitySyncResponse(BaseModel):
    """Response for activity sync operation."""
    synced_count: int
    matched_count: int
    error_count: int
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "synced_count": 15,
                "matched_count": 12,
                "error_count": 0,
                "message": "Successfully synced 15 activities, matched 12 to training days"
            }
        }


class WebhookSubscriptionRequest(BaseModel):
    """Request to create webhook subscription."""
    callback_url: str


class WebhookEventRequest(BaseModel):
    """Webhook event from Strava."""
    aspect_type: str  # create, update, delete
    event_time: int
    object_id: int
    object_type: str  # activity, athlete
    owner_id: int
    subscription_id: int
    updates: Optional[Dict[str, Any]] = None
