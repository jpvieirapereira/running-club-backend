"""
Strava Integration Use Case.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.repositories import CustomerRepository
from src.domain.entities.strava_connection import StravaConnection
from src.application.dtos.strava_dto import StravaConnectionDTO, StravaAuthDTO


class StravaIntegrationUseCase:
    """Use case for Strava OAuth integration."""
    
    def __init__(
        self,
        customer_repository: CustomerRepository,
        strava_client: 'StravaAPIClient'
    ):
        """
        Initialize use case.
        
        Args:
            customer_repository: Customer repository
            strava_client: Strava API client
        """
        self.customer_repository = customer_repository
        self.strava_client = strava_client
    
    async def get_authorization_url(
        self,
        customer_id: UUID,
        redirect_uri: str
    ) -> str:
        """
        Get Strava OAuth authorization URL.
        
        Args:
            customer_id: Customer requesting authorization
            redirect_uri: OAuth callback URL
        
        Returns:
            Authorization URL for customer to visit
        """
        # Verify customer exists
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Generate state token with customer_id for security
        state = f"{customer_id}"
        
        return self.strava_client.get_authorization_url(
            redirect_uri=redirect_uri,
            state=state
        )
    
    async def exchange_code(
        self,
        code: str,
        customer_id: UUID
    ) -> StravaConnectionDTO:
        """
        Exchange OAuth code for access token.
        
        Args:
            code: OAuth authorization code
            customer_id: Customer ID
        
        Returns:
            Strava connection info
        
        Raises:
            ValueError: If customer not found or exchange fails
        """
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Exchange code for tokens
        token_data = await self.strava_client.exchange_token(code)
        
        # Create connection entity
        connection = StravaConnection(
            customer_id=customer_id,
            athlete_id=token_data['athlete']['id'],
            access_token=token_data['access_token'],
            refresh_token=token_data['refresh_token'],
            expires_at=datetime.fromtimestamp(token_data['expires_at']),
            scope=token_data.get('scope', 'read,activity:read')
        )
        
        # Update customer with Strava info
        customer.connect_strava(connection.athlete_id)
        await self.customer_repository.update(customer)
        
        # Store connection (tokens will be stored securely)
        await self.strava_client.store_connection(connection)
        
        return StravaConnectionDTO(
            customer_id=connection.customer_id,
            athlete_id=connection.athlete_id,
            connected_at=connection.connected_at,
            scope=connection.scope
        )
    
    async def refresh_access_token(
        self,
        customer_id: UUID
    ) -> StravaConnectionDTO:
        """
        Refresh access token if needed.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            Updated connection info
        
        Raises:
            ValueError: If customer not found or not connected
        """
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        if not customer.is_strava_connected():
            raise ValueError("Customer not connected to Strava")
        
        # Get current connection
        connection = await self.strava_client.get_connection(customer_id)
        if not connection:
            raise ValueError("Connection not found")
        
        # Refresh if needed
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
        
        return StravaConnectionDTO(
            customer_id=connection.customer_id,
            athlete_id=connection.athlete_id,
            connected_at=connection.connected_at,
            last_sync_at=connection.last_sync_at,
            scope=connection.scope
        )
    
    async def disconnect(self, customer_id: UUID) -> bool:
        """
        Disconnect Strava account.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            True if disconnected successfully
        """
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Revoke Strava access
        try:
            connection = await self.strava_client.get_connection(customer_id)
            if connection:
                await self.strava_client.deauthorize(connection.access_token)
        except Exception:
            pass  # Continue even if revocation fails
        
        # Update customer
        customer.disconnect_strava()
        await self.customer_repository.update(customer)
        
        # Delete connection
        await self.strava_client.delete_connection(customer_id)
        
        return True
    
    async def get_connection_status(
        self,
        customer_id: UUID
    ) -> Optional[StravaConnectionDTO]:
        """
        Get customer's Strava connection status.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            Connection info if connected, None otherwise
        """
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer or not customer.is_strava_connected():
            return None
        
        connection = await self.strava_client.get_connection(customer_id)
        if not connection:
            return None
        
        return StravaConnectionDTO(
            customer_id=connection.customer_id,
            athlete_id=connection.athlete_id,
            connected_at=connection.connected_at,
            last_sync_at=connection.last_sync_at,
            scope=connection.scope
        )
    
    def verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        """
        Verify Strava webhook signature.
        
        Args:
            body: Request body
            signature: Signature from headers
        
        Returns:
            True if signature is valid
        """
        return self.strava_client.verify_webhook_signature(body, signature)
