"""
Strava Connection entity.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID


class StravaConnection:
    """
    Represents a customer's Strava OAuth connection.
    
    Stores OAuth tokens and connection metadata for accessing
    Strava API on behalf of a customer.
    """
    
    def __init__(
        self,
        customer_id: UUID,
        athlete_id: int,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
        scope: str,
        connected_at: Optional[datetime] = None,
        last_sync_at: Optional[datetime] = None,
    ):
        """
        Initialize a Strava connection.
        
        Args:
            customer_id: ID of the customer
            athlete_id: Strava athlete ID
            access_token: OAuth access token
            refresh_token: OAuth refresh token
            expires_at: Token expiration datetime
            scope: OAuth scope granted
            connected_at: When connection was established
            last_sync_at: Last activity sync timestamp
        """
        self.customer_id = customer_id
        self.athlete_id = athlete_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.scope = scope
        self.connected_at = connected_at or datetime.utcnow()
        self.last_sync_at = last_sync_at
    
    def is_expired(self) -> bool:
        """
        Check if access token is expired.
        
        Returns:
            True if token is expired
        """
        return datetime.utcnow() >= self.expires_at
    
    def needs_refresh(self, buffer_seconds: int = 3600) -> bool:
        """
        Check if token should be refreshed.
        
        Args:
            buffer_seconds: Refresh buffer time (default 1 hour)
        
        Returns:
            True if token should be refreshed
        """
        from datetime import timedelta
        refresh_threshold = datetime.utcnow() + timedelta(seconds=buffer_seconds)
        return self.expires_at <= refresh_threshold
    
    def update_tokens(
        self,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
    ) -> None:
        """
        Update OAuth tokens after refresh.
        
        Args:
            access_token: New access token
            refresh_token: New refresh token
            expires_at: New expiration datetime
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
    
    def update_last_sync(self) -> None:
        """Update last sync timestamp to now."""
        self.last_sync_at = datetime.utcnow()
