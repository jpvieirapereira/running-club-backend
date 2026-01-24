"""
Strava DTOs.
"""
from datetime import datetime
from typing import Optional, Dict, List, Any
from uuid import UUID
from dataclasses import dataclass

from src.domain.entities.enums import ActivityMatchStatus


@dataclass
class StravaActivityDTO:
    """DTO for Strava activity data."""
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
    match_status: ActivityMatchStatus = ActivityMatchStatus.UNMATCHED
    created_at: datetime = None


@dataclass
class StravaConnectionDTO:
    """DTO for Strava connection info."""
    customer_id: UUID
    athlete_id: int
    connected_at: datetime
    last_sync_at: Optional[datetime] = None
    scope: str = ""


@dataclass
class StravaAuthDTO:
    """DTO for Strava OAuth flow."""
    code: Optional[str] = None
    state: Optional[str] = None
    scope: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ActivitySyncResultDTO:
    """DTO for activity sync results."""
    synced_count: int
    matched_count: int
    error_count: int
    activities: List[StravaActivityDTO]
