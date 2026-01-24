from typing import Optional, List
from uuid import UUID
from datetime import datetime
from boto3.dynamodb.conditions import Key
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings


class DynamoDBUserRepository(UserRepository):
    """DynamoDB implementation of UserRepository."""
    
    def __init__(self):
        self.dynamodb = AWSClientFactory.create_dynamodb_resource()
        self.table = self.dynamodb.Table(settings.dynamodb_users_table)
    
    def _to_item(self, user: User) -> dict:
        """Convert User entity to DynamoDB item."""
        return {
            'id': str(user.id),
            'email': user.email,
            'hashed_password': user.hashed_password,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }
    
    def _from_item(self, item: dict) -> User:
        """Convert DynamoDB item to User entity."""
        user = User(
            email=item['email'],
            hashed_password=item['hashed_password'],
            full_name=item.get('full_name'),
            is_active=item.get('is_active', True),
            id=UUID(item['id'])
        )
        user.created_at = datetime.fromisoformat(item['created_at'])
        user.updated_at = datetime.fromisoformat(item['updated_at'])
        return user
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        item = self._to_item(user)
        self.table.put_item(Item=item)
        return user
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        response = self.table.get_item(Key={'id': str(user_id)})
        item = response.get('Item')
        return self._from_item(item) if item else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        response = self.table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def update(self, user: User) -> User:
        """Update existing user."""
        user.updated_at = datetime.utcnow()
        item = self._to_item(user)
        self.table.put_item(Item=item)
        return user
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID."""
        self.table.delete_item(Key={'id': str(user_id)})
        return True
    
    async def list_all(self) -> List[User]:
        """List all users."""
        response = self.table.scan()
        items = response.get('Items', [])
        return [self._from_item(item) for item in items]
