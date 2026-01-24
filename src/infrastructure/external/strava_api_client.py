"""
Strava API Client.
"""
import hmac
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID

import httpx

from src.domain.entities.strava_connection import StravaConnection


class StravaAPIClient:
    """Client for interacting with Strava API."""
    
    BASE_URL = "https://www.strava.com/api/v3"
    AUTH_URL = "https://www.strava.com/oauth/authorize"
    TOKEN_URL = "https://www.strava.com/oauth/token"
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        webhook_verify_token: str
    ):
        """
        Initialize Strava API client.
        
        Args:
            client_id: Strava application client ID
            client_secret: Strava application client secret
            webhook_verify_token: Token for webhook verification
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.webhook_verify_token = webhook_verify_token
        self._connections: Dict[UUID, StravaConnection] = {}
    
    def get_authorization_url(
        self,
        redirect_uri: str,
        state: str,
        scope: str = "read,activity:read"
    ) -> str:
        """
        Get OAuth authorization URL.
        
        Args:
            redirect_uri: Callback URL
            state: State parameter for CSRF protection
            scope: OAuth scopes
        
        Returns:
            Authorization URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state
        }
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query_string}"
    
    async def exchange_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code
        
        Returns:
            Token response with access_token, refresh_token, expires_at, athlete
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code"
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token.
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            Token response with new access_token, refresh_token, expires_at
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def deauthorize(self, access_token: str) -> None:
        """
        Revoke access token.
        
        Args:
            access_token: Access token to revoke
        """
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.BASE_URL}/oauth/deauthorize",
                headers={"Authorization": f"Bearer {access_token}"}
            )
    
    async def get_athlete_activities(
        self,
        access_token: str,
        after: Optional[datetime] = None,
        per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get athlete's activities.
        
        Args:
            access_token: OAuth access token
            after: Only activities after this date
            per_page: Results per page
        
        Returns:
            List of activity summaries
        """
        params = {"per_page": per_page}
        if after:
            params["after"] = int(after.timestamp())
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/athlete/activities",
                headers={"Authorization": f"Bearer {access_token}"},
                params=params
            )
            response.raise_for_status()
            return response.json()
    
    async def get_activity_detail(
        self,
        access_token: str,
        activity_id: int
    ) -> Dict[str, Any]:
        """
        Get detailed activity data.
        
        Args:
            access_token: OAuth access token
            activity_id: Strava activity ID
        
        Returns:
            Detailed activity data
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/activities/{activity_id}",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"include_all_efforts": "true"}
            )
            response.raise_for_status()
            return response.json()
    
    def verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        """
        Verify Strava webhook signature (not currently implemented by Strava).
        
        For now, just verify the verify_token in subscription.
        
        Args:
            body: Request body
            signature: Signature header
        
        Returns:
            True if valid
        """
        # Strava doesn't currently sign webhooks
        # This would be where you'd verify HMAC if they did
        return True
    
    async def store_connection(self, connection: StravaConnection) -> None:
        """
        Store connection in memory (in production, use database or secure storage).
        
        Args:
            connection: Strava connection to store
        """
        self._connections[connection.customer_id] = connection
    
    async def get_connection(
        self,
        customer_id: UUID
    ) -> Optional[StravaConnection]:
        """
        Get stored connection.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            Connection if found
        """
        return self._connections.get(customer_id)
    
    async def delete_connection(self, customer_id: UUID) -> None:
        """
        Delete stored connection.
        
        Args:
            customer_id: Customer ID
        """
        self._connections.pop(customer_id, None)
    
    async def create_webhook_subscription(
        self,
        callback_url: str
    ) -> Dict[str, Any]:
        """
        Create webhook subscription with Strava.
        
        Args:
            callback_url: URL for webhook events
        
        Returns:
            Subscription data
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.strava.com/api/v3/push_subscriptions",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "callback_url": callback_url,
                    "verify_token": self.webhook_verify_token
                }
            )
            response.raise_for_status()
            return response.json()
