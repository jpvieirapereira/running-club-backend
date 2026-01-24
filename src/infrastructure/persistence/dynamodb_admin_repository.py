"""
DynamoDB Admin Repository implementation.
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from boto3.dynamodb.conditions import Key, Attr

from src.domain.entities.admin import Admin
from src.domain.entities.enums import UserType
from src.domain.repositories.admin_repository import AdminRepository
from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings


class DynamoDBAdminRepository(AdminRepository):
    """DynamoDB implementation of AdminRepository."""
    
    def __init__(self):
        self.dynamodb = AWSClientFactory.create_dynamodb_resource()
        self.table = self.dynamodb.Table(settings.dynamodb_users_table)
    
    def _to_item(self, admin: Admin) -> dict:
        """Convert Admin entity to DynamoDB item."""
        item = {
            'id': str(admin.id),
            'email': admin.email,
            'hashed_password': admin.hashed_password,
            'name': admin.name,
            'phone': admin.phone,
            'date_of_birth': admin.date_of_birth.isoformat(),
            'user_type': UserType.ADMIN.value,
            'is_active': admin.is_active,
            'created_at': admin.created_at.isoformat(),
            'updated_at': admin.updated_at.isoformat()
        }
        
        if admin.nickname:
            item['nickname'] = admin.nickname
        
        return item
    
    def _from_item(self, item: dict) -> Admin:
        """Convert DynamoDB item to Admin entity."""
        admin = Admin(
            email=item['email'],
            hashed_password=item['hashed_password'],
            name=item['name'],
            phone=item['phone'],
            date_of_birth=date.fromisoformat(item['date_of_birth']),
            nickname=item.get('nickname'),
            is_active=item.get('is_active', True),
            id=UUID(item['id'])
        )
        admin.created_at = datetime.fromisoformat(item['created_at'])
        admin.updated_at = datetime.fromisoformat(item['updated_at'])
        return admin
    
    async def create(self, admin: Admin) -> Admin:
        """Create a new admin."""
        item = self._to_item(admin)
        self.table.put_item(Item=item)
        return admin
    
    async def get_by_id(self, admin_id: UUID) -> Optional[Admin]:
        """Get admin by ID."""
        response = self.table.get_item(Key={'id': str(admin_id)})
        item = response.get('Item')
        return self._from_item(item) if item else None
    
    async def get_by_email(self, email: str) -> Optional[Admin]:
        """Get admin by email."""
        response = self.table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email),
            FilterExpression=Attr('user_type').eq(UserType.ADMIN.value)
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def get_all(self) -> List[Admin]:
        """Get all admins."""
        response = self.table.scan(
            FilterExpression=Attr('user_type').eq(UserType.ADMIN.value)
        )
        return [self._from_item(item) for item in response.get('Items', [])]
    
    async def update(self, admin: Admin) -> Admin:
        """Update an existing admin."""
        admin.updated_at = datetime.utcnow()
        item = self._to_item(admin)
        self.table.put_item(Item=item)
        return admin
    
    async def delete(self, admin_id: UUID) -> bool:
        """Delete an admin."""
        try:
            self.table.delete_item(Key={'id': str(admin_id)})
            return True
        except Exception:
            return False
