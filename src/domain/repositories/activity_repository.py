"""
Activity repository interface.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.entities.strava_activity import StravaActivity
from src.domain.entities.enums import ActivityMatchStatus


class ActivityRepository(ABC):
    """Repository interface for Strava activities."""
    
    @abstractmethod
    async def create(self, activity: StravaActivity) -> StravaActivity:
        """
        Create a new activity.
        
        Args:
            activity: Activity to create
        
        Returns:
            Created activity
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, activity_id: UUID) -> Optional[StravaActivity]:
        """
        Get activity by ID.
        
        Args:
            activity_id: Activity unique identifier
        
        Returns:
            Activity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_strava_id(
        self,
        strava_activity_id: int,
        customer_id: UUID
    ) -> Optional[StravaActivity]:
        """
        Get activity by Strava activity ID.
        
        Args:
            strava_activity_id: Strava activity ID
            customer_id: Customer ID
        
        Returns:
            Activity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_customer(
        self,
        customer_id: UUID,
        limit: int = 100
    ) -> List[StravaActivity]:
        """
        Get all activities for a customer.
        
        Args:
            customer_id: Customer unique identifier
            limit: Maximum number of activities to return
        
        Returns:
            List of activities
        """
        pass
    
    @abstractmethod
    async def get_by_date_range(
        self,
        customer_id: UUID,
        start_date: datetime,
        end_date: datetime
    ) -> List[StravaActivity]:
        """
        Get activities within a date range.
        
        Args:
            customer_id: Customer unique identifier
            start_date: Start of date range
            end_date: End of date range
        
        Returns:
            List of activities in range
        """
        pass
    
    @abstractmethod
    async def get_unmatched_activities(
        self,
        customer_id: UUID
    ) -> List[StravaActivity]:
        """
        Get all unmatched activities for a customer.
        
        Args:
            customer_id: Customer unique identifier
        
        Returns:
            List of unmatched activities
        """
        pass
    
    @abstractmethod
    async def update(self, activity: StravaActivity) -> StravaActivity:
        """
        Update an existing activity.
        
        Args:
            activity: Activity with updated data
        
        Returns:
            Updated activity
        """
        pass
    
    @abstractmethod
    async def update_match_status(
        self,
        activity_id: UUID,
        training_day_id: Optional[UUID],
        match_status: ActivityMatchStatus
    ) -> None:
        """
        Update activity matching status.
        
        Args:
            activity_id: Activity unique identifier
            training_day_id: Training day ID (if matched)
            match_status: New match status
        """
        pass
    
    @abstractmethod
    async def delete(self, activity_id: UUID) -> bool:
        """
        Delete an activity.
        
        Args:
            activity_id: Activity unique identifier
        
        Returns:
            True if deleted, False if not found
        """
        pass
