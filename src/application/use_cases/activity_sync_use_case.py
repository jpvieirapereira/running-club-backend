"""
Activity Sync Use Case.
"""
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from src.domain.repositories import ActivityRepository, CustomerRepository
from src.domain.entities.strava_activity import StravaActivity
from src.domain.entities.enums import ActivityMatchStatus
from src.application.dtos.strava_dto import StravaActivityDTO, ActivitySyncResultDTO


class ActivitySyncUseCase:
    """Use case for syncing and matching Strava activities."""
    
    def __init__(
        self,
        activity_repository: ActivityRepository,
        customer_repository: CustomerRepository,
        training_plan_repository: 'TrainingPlanRepository',
        strava_client: 'StravaAPIClient'
    ):
        """
        Initialize use case.
        
        Args:
            activity_repository: Activity repository
            customer_repository: Customer repository
            training_plan_repository: Training plan repository
            strava_client: Strava API client
        """
        self.activity_repository = activity_repository
        self.customer_repository = customer_repository
        self.training_plan_repository = training_plan_repository
        self.strava_client = strava_client
    
    async def sync_activities(
        self,
        customer_id: UUID,
        after_date: Optional[datetime] = None
    ) -> ActivitySyncResultDTO:
        """
        Sync activities from Strava.
        
        Args:
            customer_id: Customer ID
            after_date: Only sync activities after this date
        
        Returns:
            Sync results with counts and activities
        """
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        if not customer.is_strava_connected():
            raise ValueError("Customer not connected to Strava")
        
        # Get connection
        connection = await self.strava_client.get_connection(customer_id)
        if not connection:
            raise ValueError("Connection not found")
        
        # Refresh token if needed
        if connection.needs_refresh():
            token_data = await self.strava_client.refresh_token(
                connection.refresh_token
            )
            connection.update_tokens(
                access_token=token_data['access_token'],
                refresh_token=token_data['refresh_token'],
                expires_at=datetime.fromtimestamp(token_data['expires_at'])
            )
            await self.strava_client.store_connection(connection)
        
        # Default to last 30 days if no after_date provided
        if not after_date:
            after_date = datetime.utcnow() - timedelta(days=30)
        
        # Fetch activities from Strava
        strava_activities = await self.strava_client.get_athlete_activities(
            access_token=connection.access_token,
            after=after_date
        )
        
        synced_count = 0
        error_count = 0
        activities: List[StravaActivityDTO] = []
        
        for strava_activity in strava_activities:
            try:
                # Check if already exists
                existing = await self.activity_repository.get_by_strava_id(
                    strava_activity['id'],
                    customer_id
                )
                
                if existing:
                    continue  # Skip duplicates
                
                # Create activity entity
                activity = self._strava_data_to_entity(
                    strava_activity,
                    customer_id
                )
                
                # Store activity
                created = await self.activity_repository.create(activity)
                synced_count += 1
                
                activities.append(self._entity_to_dto(created))
                
            except Exception as e:
                error_count += 1
                # Log error but continue processing
                continue
        
        # Update last sync timestamp
        customer.update_last_sync()
        await self.customer_repository.update(customer)
        
        # Auto-match activities to training days
        matched_count = await self.match_activities_to_training_days(customer_id)
        
        return ActivitySyncResultDTO(
            synced_count=synced_count,
            matched_count=matched_count,
            error_count=error_count,
            activities=activities
        )
    
    async def sync_single_activity(
        self,
        strava_activity_id: int,
        customer_id: UUID
    ) -> StravaActivityDTO:
        """
        Sync a single activity from Strava.
        
        Args:
            strava_activity_id: Strava activity ID
            customer_id: Customer ID
        
        Returns:
            Synced activity
        """
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer or not customer.is_strava_connected():
            raise ValueError("Customer not connected to Strava")
        
        # Get connection
        connection = await self.strava_client.get_connection(customer_id)
        if not connection:
            raise ValueError("Connection not found")
        
        # Fetch activity detail from Strava
        strava_activity = await self.strava_client.get_activity_detail(
            access_token=connection.access_token,
            activity_id=strava_activity_id
        )
        
        # Check if already exists
        existing = await self.activity_repository.get_by_strava_id(
            strava_activity_id,
            customer_id
        )
        
        if existing:
            # Update existing
            activity = self._strava_data_to_entity(strava_activity, customer_id)
            activity.id = existing.id
            updated = await self.activity_repository.update(activity)
            return self._entity_to_dto(updated)
        else:
            # Create new
            activity = self._strava_data_to_entity(strava_activity, customer_id)
            created = await self.activity_repository.create(activity)
            
            # Try to match
            await self._match_single_activity(created)
            
            return self._entity_to_dto(created)
    
    async def match_activities_to_training_days(
        self,
        customer_id: UUID
    ) -> int:
        """
        Auto-match unmatched activities to training days by date.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            Number of activities matched
        """
        # Get unmatched activities
        unmatched = await self.activity_repository.get_unmatched_activities(
            customer_id
        )
        
        matched_count = 0
        
        for activity in unmatched:
            if await self._match_single_activity(activity):
                matched_count += 1
        
        return matched_count
    
    async def _match_single_activity(self, activity: StravaActivity) -> bool:
        """
        Match a single activity to a training day.
        
        Args:
            activity: Activity to match
        
        Returns:
            True if matched
        """
        # Get training days for this customer on activity date
        activity_date = activity.start_date.date()
        
        # Get all plans for customer
        plans = await self.training_plan_repository.get_by_customer_id(
            activity.customer_id
        )
        
        for plan in plans:
            # Get training days for this date
            training_days = await self.training_plan_repository.get_training_days(
                plan.id
            )
            
            for day in training_days:
                # Match by date and unmatched status
                if day.date == activity_date and not day.matched_activity_id:
                    # Match them
                    activity.match_to_training_day(day.id)
                    await self.activity_repository.update(activity)
                    return True
        
        return False
    
    async def get_customer_activities(
        self,
        customer_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        match_status: Optional[ActivityMatchStatus] = None,
        limit: int = 100
    ) -> List[StravaActivityDTO]:
        """
        Get customer's activities with optional filters.
        
        Args:
            customer_id: Customer ID
            start_date: Filter by start date
            end_date: Filter by end date
            match_status: Filter by match status
            limit: Maximum results
        
        Returns:
            List of activities
        """
        if start_date and end_date:
            activities = await self.activity_repository.get_by_date_range(
                customer_id,
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.max.time())
            )
        else:
            activities = await self.activity_repository.get_by_customer(
                customer_id,
                limit
            )
        
        # Apply match status filter if provided
        if match_status:
            activities = [a for a in activities if a.match_status == match_status]
        
        return [self._entity_to_dto(a) for a in activities]
    
    async def get_activity_by_id(
        self,
        activity_id: UUID,
        requesting_user_id: UUID,
        requesting_user_type: str
    ) -> Optional[StravaActivityDTO]:
        """
        Get activity detail with access control.
        
        Args:
            activity_id: Activity ID
            requesting_user_id: User requesting access
            requesting_user_type: Type of user (coach/customer)
        
        Returns:
            Activity if authorized, None otherwise
        """
        activity = await self.activity_repository.get_by_id(activity_id)
        if not activity:
            return None
        
        # Check access: customer owns it, or coach of customer
        if requesting_user_type == "customer":
            if activity.customer_id != requesting_user_id:
                return None
        elif requesting_user_type == "coach":
            customer = await self.customer_repository.get_by_id(activity.customer_id)
            if not customer or customer.coach_id != requesting_user_id:
                return None
        else:
            return None
        
        return self._entity_to_dto(activity)
    
    def _strava_data_to_entity(
        self,
        data: Dict[str, Any],
        customer_id: UUID
    ) -> StravaActivity:
        """Convert Strava API data to entity."""
        return StravaActivity(
            customer_id=customer_id,
            strava_activity_id=data['id'],
            name=data.get('name', 'Untitled'),
            activity_type=data.get('type', 'Run'),
            start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
            distance=data.get('distance', 0),
            moving_time=data.get('moving_time', 0),
            elapsed_time=data.get('elapsed_time', 0),
            total_elevation_gain=data.get('total_elevation_gain'),
            average_speed=data.get('average_speed'),
            max_speed=data.get('max_speed'),
            average_heartrate=data.get('average_heartrate'),
            max_heartrate=data.get('max_heartrate'),
            heartrate_zones=data.get('heartrate_zones'),
            splits=data.get('splits_metric'),
            laps=data.get('laps'),
            calories=data.get('calories'),
            suffer_score=data.get('suffer_score'),
            kudos_count=data.get('kudos_count', 0),
            comment_count=data.get('comment_count', 0),
            achievement_count=data.get('achievement_count', 0),
            photos=self._extract_photo_urls(data.get('photos', {})),
            map_polyline=data.get('map', {}).get('summary_polyline')
        )
    
    def _extract_photo_urls(self, photos_data: Dict) -> List[str]:
        """Extract photo URLs from Strava photos data."""
        urls = []
        if photos_data.get('primary'):
            urls.append(photos_data['primary'].get('urls', {}).get('600'))
        return [url for url in urls if url]
    
    def _entity_to_dto(self, activity: StravaActivity) -> StravaActivityDTO:
        """Convert entity to DTO."""
        return StravaActivityDTO(
            id=activity.id,
            customer_id=activity.customer_id,
            strava_activity_id=activity.strava_activity_id,
            name=activity.name,
            activity_type=activity.activity_type,
            start_date=activity.start_date,
            distance=activity.distance,
            moving_time=activity.moving_time,
            elapsed_time=activity.elapsed_time,
            total_elevation_gain=activity.total_elevation_gain,
            average_speed=activity.average_speed,
            max_speed=activity.max_speed,
            average_pace=activity.average_pace,
            average_heartrate=activity.average_heartrate,
            max_heartrate=activity.max_heartrate,
            heartrate_zones=activity.heartrate_zones,
            splits=activity.splits,
            laps=activity.laps,
            calories=activity.calories,
            suffer_score=activity.suffer_score,
            kudos_count=activity.kudos_count,
            comment_count=activity.comment_count,
            achievement_count=activity.achievement_count,
            photos=activity.photos,
            map_polyline=activity.map_polyline,
            training_day_id=activity.training_day_id,
            match_status=activity.match_status,
            created_at=activity.created_at
        )
