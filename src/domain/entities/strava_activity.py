"""
Strava Activity entity.
"""
from datetime import datetime
from typing import Optional, Dict, List, Any
from uuid import UUID, uuid4

from .enums import ActivityMatchStatus


class StravaActivity:
    """
    Represents a Strava activity with full data.
    
    Stores comprehensive activity data from Strava API including
    performance metrics, heart rate zones, GPS data, and social interactions.
    """
    
    def __init__(
        self,
        customer_id: UUID,
        strava_activity_id: int,
        name: str,
        activity_type: str,
        start_date: datetime,
        distance: float,
        moving_time: int,
        elapsed_time: int,
        id: Optional[UUID] = None,
        total_elevation_gain: Optional[float] = None,
        average_speed: Optional[float] = None,
        max_speed: Optional[float] = None,
        average_pace: Optional[float] = None,
        average_heartrate: Optional[float] = None,
        max_heartrate: Optional[float] = None,
        heartrate_zones: Optional[Dict[str, Any]] = None,
        splits: Optional[List[Dict[str, Any]]] = None,
        laps: Optional[List[Dict[str, Any]]] = None,
        calories: Optional[float] = None,
        suffer_score: Optional[float] = None,
        kudos_count: int = 0,
        comment_count: int = 0,
        achievement_count: int = 0,
        photos: Optional[List[str]] = None,
        map_polyline: Optional[str] = None,
        training_day_id: Optional[UUID] = None,
        match_status: ActivityMatchStatus = ActivityMatchStatus.UNMATCHED,
        created_at: Optional[datetime] = None,
    ):
        """
        Initialize a Strava activity.
        
        Args:
            customer_id: ID of the customer who owns this activity
            strava_activity_id: Original Strava activity ID
            name: Activity name/title
            activity_type: Type of activity (Run, Trail Run, etc.)
            start_date: Activity start date/time
            distance: Distance in meters
            moving_time: Moving time in seconds
            elapsed_time: Elapsed time in seconds
            id: Unique identifier (auto-generated if not provided)
            total_elevation_gain: Total elevation gain in meters
            average_speed: Average speed in m/s
            max_speed: Maximum speed in m/s
            average_pace: Average pace in min/km
            average_heartrate: Average heart rate in BPM
            max_heartrate: Maximum heart rate in BPM
            heartrate_zones: Heart rate zones distribution
            splits: Kilometer/mile splits data
            laps: Lap data if available
            calories: Calories burned
            suffer_score: Strava suffer score
            kudos_count: Number of kudos received
            comment_count: Number of comments
            achievement_count: Number of achievements
            photos: List of photo URLs
            map_polyline: Encoded polyline for GPS track
            training_day_id: ID of matched training day (if any)
            match_status: Status of matching to training day
            created_at: Activity creation timestamp
        """
        self.id = id or uuid4()
        self.customer_id = customer_id
        self.strava_activity_id = strava_activity_id
        self.name = name
        self.activity_type = activity_type
        self.start_date = start_date
        self.distance = distance
        self.moving_time = moving_time
        self.elapsed_time = elapsed_time
        self.total_elevation_gain = total_elevation_gain
        self.average_speed = average_speed
        self.max_speed = max_speed
        self.average_pace = average_pace
        self.average_heartrate = average_heartrate
        self.max_heartrate = max_heartrate
        self.heartrate_zones = heartrate_zones or {}
        self.splits = splits or []
        self.laps = laps or []
        self.calories = calories
        self.suffer_score = suffer_score
        self.kudos_count = kudos_count
        self.comment_count = comment_count
        self.achievement_count = achievement_count
        self.photos = photos or []
        self.map_polyline = map_polyline
        self.training_day_id = training_day_id
        self.match_status = match_status
        self.created_at = created_at or datetime.utcnow()
    
    def match_to_training_day(self, training_day_id: UUID) -> None:
        """
        Match this activity to a training day.
        
        Args:
            training_day_id: ID of the training day to match
        """
        self.training_day_id = training_day_id
        self.match_status = ActivityMatchStatus.MATCHED
    
    def unmatch(self) -> None:
        """Remove matching from training day."""
        self.training_day_id = None
        self.match_status = ActivityMatchStatus.UNMATCHED
    
    def ignore(self) -> None:
        """Mark activity as ignored (won't be auto-matched)."""
        self.match_status = ActivityMatchStatus.IGNORED
    
    def calculate_pace_min_per_km(self) -> Optional[float]:
        """
        Calculate average pace in minutes per kilometer.
        
        Returns:
            Pace in minutes per km, or None if data unavailable
        """
        if self.distance > 0 and self.moving_time > 0:
            # Convert meters to km, seconds to minutes
            km = self.distance / 1000
            minutes = self.moving_time / 60
            return minutes / km
        return None
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the activity for display.
        
        Returns:
            Dictionary with key activity metrics
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.activity_type,
            "date": self.start_date.isoformat(),
            "distance_km": round(self.distance / 1000, 2),
            "duration_minutes": round(self.moving_time / 60, 1),
            "pace_min_per_km": self.calculate_pace_min_per_km(),
            "elevation_gain_m": self.total_elevation_gain,
            "matched": self.match_status == ActivityMatchStatus.MATCHED,
        }
