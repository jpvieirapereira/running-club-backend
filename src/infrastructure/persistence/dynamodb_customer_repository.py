from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from boto3.dynamodb.conditions import Key, Attr
from src.domain.entities.customer import Customer
from src.domain.entities.enums import UserType, RunnerLevel, TrainingAvailability
from src.domain.repositories.customer_repository import CustomerRepository
from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings


class DynamoDBCustomerRepository(CustomerRepository):
    """DynamoDB implementation of CustomerRepository."""
    
    def __init__(self):
        self.dynamodb = AWSClientFactory.create_dynamodb_resource()
        self.table = self.dynamodb.Table(settings.dynamodb_users_table)
    
    def _to_item(self, customer: Customer) -> dict:
        """Convert Customer entity to DynamoDB item."""
        item = {
            'id': str(customer.id),
            'email': customer.email,
            'hashed_password': customer.hashed_password,
            'name': customer.name,
            'phone': customer.phone,
            'date_of_birth': customer.date_of_birth.isoformat(),
            'document_number': customer.document_number,
            'user_type': UserType.CUSTOMER.value,
            'is_active': customer.is_active,
            'created_at': customer.created_at.isoformat(),
            'updated_at': customer.updated_at.isoformat()
        }
        
        # Add optional fields only if they have values
        if customer.nickname:
            item['nickname'] = customer.nickname
        if customer.runner_level:
            item['runner_level'] = customer.runner_level.value
        if customer.training_availability:
            item['training_availability'] = customer.training_availability.value
        if customer.challenge_next_month:
            item['challenge_next_month'] = customer.challenge_next_month
        if customer.coach_id:
            item['coach_id'] = str(customer.coach_id)
        if customer.strava_athlete_id:
            item['strava_athlete_id'] = customer.strava_athlete_id
        if customer.strava_connected_at:
            item['strava_connected_at'] = customer.strava_connected_at.isoformat()
        if customer.strava_last_sync:
            item['strava_last_sync'] = customer.strava_last_sync.isoformat()
        
        return item
    
    def _from_item(self, item: dict) -> Customer:
        """Convert DynamoDB item to Customer entity."""
        customer = Customer(
            email=item['email'],
            hashed_password=item['hashed_password'],
            name=item['name'],
            phone=item['phone'],
            date_of_birth=date.fromisoformat(item['date_of_birth']),
            document_number=item['document_number'],
            runner_level=RunnerLevel(item['runner_level']) if item.get('runner_level') else None,
            training_availability=TrainingAvailability(item['training_availability']) if item.get('training_availability') else None,
            challenge_next_month=item.get('challenge_next_month'),
            coach_id=UUID(item['coach_id']) if item.get('coach_id') else None,
            strava_athlete_id=item.get('strava_athlete_id'),
            strava_connected_at=datetime.fromisoformat(item['strava_connected_at']) if item.get('strava_connected_at') else None,
            strava_last_sync=datetime.fromisoformat(item['strava_last_sync']) if item.get('strava_last_sync') else None,
            nickname=item.get('nickname'),
            is_active=item.get('is_active', True),
            id=UUID(item['id'])
        )
        customer.created_at = datetime.fromisoformat(item['created_at'])
        customer.updated_at = datetime.fromisoformat(item['updated_at'])
        return customer
    
    async def create(self, customer: Customer) -> Customer:
        """Create a new customer."""
        item = self._to_item(customer)
        self.table.put_item(Item=item)
        return customer
    
    async def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """Get customer by ID."""
        response = self.table.get_item(Key={'id': str(customer_id)})
        item = response.get('Item')
        if item and item.get('user_type') == UserType.CUSTOMER.value:
            return self._from_item(item)
        return None
    
    async def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        response = self.table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email),
            FilterExpression=Attr('user_type').eq(UserType.CUSTOMER.value)
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def get_by_document_number(self, document_number: str) -> Optional[Customer]:
        """Get customer by CPF."""
        response = self.table.scan(
            FilterExpression=Attr('document_number').eq(document_number) & 
                           Attr('user_type').eq(UserType.CUSTOMER.value)
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def get_by_coach_id(self, coach_id: UUID) -> List[Customer]:
        """Get all customers assigned to a coach."""
        response = self.table.scan(
            FilterExpression=Attr('coach_id').eq(str(coach_id)) & 
                           Attr('user_type').eq(UserType.CUSTOMER.value)
        )
        items = response.get('Items', [])
        return [self._from_item(item) for item in items]
    
    async def update(self, customer: Customer) -> Customer:
        """Update existing customer."""
        customer.updated_at = datetime.utcnow()
        item = self._to_item(customer)
        self.table.put_item(Item=item)
        return customer
    
    async def delete(self, customer_id: UUID) -> bool:
        """Delete customer by ID."""
        self.table.delete_item(Key={'id': str(customer_id)})
        return True
    
    async def list_all(self) -> List[Customer]:
        """List all customers."""
        response = self.table.scan(
            FilterExpression=Attr('user_type').eq(UserType.CUSTOMER.value)
        )
        items = response.get('Items', [])
        return [self._from_item(item) for item in items]
