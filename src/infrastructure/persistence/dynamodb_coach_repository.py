from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from boto3.dynamodb.conditions import Key, Attr
from src.domain.entities.coach import Coach
from src.domain.entities.enums import UserType
from src.domain.repositories.coach_repository import CoachRepository
from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings


class DynamoDBCoachRepository(CoachRepository):
    """DynamoDB implementation of CoachRepository."""
    
    def __init__(self):
        self.dynamodb = AWSClientFactory.create_dynamodb_resource()
        self.table = self.dynamodb.Table(settings.dynamodb_users_table)
    
    def _to_item(self, coach: Coach) -> dict:
        """Convert Coach entity to DynamoDB item."""
        item = {
            'id': str(coach.id),
            'email': coach.email,
            'hashed_password': coach.hashed_password,
            'name': coach.name,
            'phone': coach.phone,
            'date_of_birth': coach.date_of_birth.isoformat(),
            'document_number': coach.document_number,
            'user_type': UserType.COACH.value,
            'is_active': coach.is_active,
            'created_at': coach.created_at.isoformat(),
            'updated_at': coach.updated_at.isoformat()
        }
        
        # Add optional fields only if they have values
        if coach.nickname:
            item['nickname'] = coach.nickname
        if coach.bio:
            item['bio'] = coach.bio
        if coach.specialization:
            item['specialization'] = coach.specialization
        
        return item
    
    def _from_item(self, item: dict) -> Coach:
        """Convert DynamoDB item to Coach entity."""
        coach = Coach(
            email=item['email'],
            hashed_password=item['hashed_password'],
            name=item['name'],
            phone=item['phone'],
            date_of_birth=date.fromisoformat(item['date_of_birth']),
            document_number=item['document_number'],
            bio=item.get('bio'),
            specialization=item.get('specialization'),
            nickname=item.get('nickname'),
            is_active=item.get('is_active', True),
            id=UUID(item['id'])
        )
        coach.created_at = datetime.fromisoformat(item['created_at'])
        coach.updated_at = datetime.fromisoformat(item['updated_at'])
        return coach
    
    async def create(self, coach: Coach) -> Coach:
        """Create a new coach."""
        item = self._to_item(coach)
        self.table.put_item(Item=item)
        return coach
    
    async def get_by_id(self, coach_id: UUID) -> Optional[Coach]:
        """Get coach by ID."""
        response = self.table.get_item(Key={'id': str(coach_id)})
        item = response.get('Item')
        if item and item.get('user_type') == UserType.COACH.value:
            return self._from_item(item)
        return None
    
    async def get_by_email(self, email: str) -> Optional[Coach]:
        """Get coach by email."""
        response = self.table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email),
            FilterExpression=Attr('user_type').eq(UserType.COACH.value)
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def get_by_document_number(self, document_number: str) -> Optional[Coach]:
        """Get coach by CNPJ."""
        response = self.table.scan(
            FilterExpression=Attr('document_number').eq(document_number) & 
                           Attr('user_type').eq(UserType.COACH.value)
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def update(self, coach: Coach) -> Coach:
        """Update existing coach."""
        coach.updated_at = datetime.utcnow()
        item = self._to_item(coach)
        self.table.put_item(Item=item)
        return coach
    
    async def delete(self, coach_id: UUID) -> bool:
        """Delete coach by ID."""
        self.table.delete_item(Key={'id': str(coach_id)})
        return True
    
    async def list_all(self) -> List[Coach]:
        """List all coaches."""
        response = self.table.scan(
            FilterExpression=Attr('user_type').eq(UserType.COACH.value)
        )
        items = response.get('Items', [])
        return [self._from_item(item) for item in items]
