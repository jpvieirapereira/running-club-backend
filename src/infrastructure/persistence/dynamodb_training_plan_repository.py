from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from boto3.dynamodb.conditions import Key, Attr
from src.domain.entities.training_plan import TrainingPlan
from src.domain.entities.training_day import TrainingDay
from src.domain.entities.enums import TrainingType, TrainingZone, TerrainType
from src.domain.repositories.training_plan_repository import TrainingPlanRepository
from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings


class DynamoDBTrainingPlanRepository(TrainingPlanRepository):
    """DynamoDB implementation of TrainingPlanRepository."""
    
    def __init__(self):
        self.dynamodb = AWSClientFactory.create_dynamodb_resource()
        self.table = self.dynamodb.Table(settings.dynamodb_training_plans_table)
    
    def _plan_to_item(self, plan: TrainingPlan) -> dict:
        """Convert TrainingPlan entity to DynamoDB item."""
        item = {
            'pk': f"PLAN#{str(plan.id)}",
            'sk': 'METADATA',
            'id': str(plan.id),
            'coach_id': str(plan.coach_id),
            'customer_id': str(plan.customer_id),
            'name': plan.name,
            'start_date': plan.start_date.isoformat(),
            'end_date': plan.end_date.isoformat(),
            'is_active': plan.is_active,
            'created_at': plan.created_at.isoformat(),
            'updated_at': plan.updated_at.isoformat(),
            'entity_type': 'training_plan'
        }
        
        if plan.description:
            item['description'] = plan.description
        if plan.success_criteria:
            item['success_criteria'] = plan.success_criteria
        
        return item
    
    def _item_to_plan(self, item: dict) -> TrainingPlan:
        """Convert DynamoDB item to TrainingPlan entity."""
        plan = TrainingPlan(
            coach_id=UUID(item['coach_id']),
            customer_id=UUID(item['customer_id']),
            name=item['name'],
            start_date=date.fromisoformat(item['start_date']),
            end_date=date.fromisoformat(item['end_date']),
            description=item.get('description'),
            success_criteria=item.get('success_criteria'),
            is_active=item.get('is_active', True),
            id=UUID(item['id'])
        )
        plan.created_at = datetime.fromisoformat(item['created_at'])
        plan.updated_at = datetime.fromisoformat(item['updated_at'])
        return plan
    
    def _day_to_item(self, day: TrainingDay) -> dict:
        """Convert TrainingDay entity to DynamoDB item."""
        return {
            'pk': f"PLAN#{str(day.training_plan_id)}",
            'sk': f"DAY#{day.date.isoformat()}#{str(day.id)}",
            'id': str(day.id),
            'training_plan_id': str(day.training_plan_id),
            'date': day.date.isoformat(),
            'training_type': day.training_type.value,
            'zone': day.zone.value,
            'terrain': day.terrain.value,
            'distance_km': str(day.distance_km),
            'workout_details': day.workout_details,
            'day_order': day.day_order,
            'created_at': day.created_at.isoformat(),
            'updated_at': day.updated_at.isoformat(),
            'entity_type': 'training_day'
        }
    
    def _item_to_day(self, item: dict) -> TrainingDay:
        """Convert DynamoDB item to TrainingDay entity."""
        day = TrainingDay(
            training_plan_id=UUID(item['training_plan_id']),
            date=date.fromisoformat(item['date']),
            training_type=TrainingType(item['training_type']),
            zone=TrainingZone(item['zone']),
            terrain=TerrainType(item['terrain']),
            distance_km=float(item['distance_km']),
            workout_details=item['workout_details'],
            day_order=item['day_order'],
            id=UUID(item['id'])
        )
        day.created_at = datetime.fromisoformat(item['created_at'])
        day.updated_at = datetime.fromisoformat(item['updated_at'])
        return day
    
    async def create(self, training_plan: TrainingPlan) -> TrainingPlan:
        """Create a new training plan."""
        item = self._plan_to_item(training_plan)
        self.table.put_item(Item=item)
        return training_plan
    
    async def get_by_id(self, plan_id: UUID) -> Optional[TrainingPlan]:
        """Get training plan by ID."""
        response = self.table.get_item(
            Key={
                'pk': f"PLAN#{str(plan_id)}",
                'sk': 'METADATA'
            }
        )
        item = response.get('Item')
        return self._item_to_plan(item) if item else None
    
    async def update(self, training_plan: TrainingPlan) -> TrainingPlan:
        """Update existing training plan."""
        training_plan.updated_at = datetime.utcnow()
        item = self._plan_to_item(training_plan)
        self.table.put_item(Item=item)
        return training_plan
    
    async def delete(self, plan_id: UUID) -> bool:
        """Delete training plan and all its training days."""
        # Delete plan metadata
        self.table.delete_item(
            Key={
                'pk': f"PLAN#{str(plan_id)}",
                'sk': 'METADATA'
            }
        )
        
        # Delete all training days
        response = self.table.query(
            KeyConditionExpression=Key('pk').eq(f"PLAN#{str(plan_id)}") & 
                                 Key('sk').begins_with('DAY#')
        )
        
        for item in response.get('Items', []):
            self.table.delete_item(
                Key={
                    'pk': item['pk'],
                    'sk': item['sk']
                }
            )
        
        return True
    
    async def get_by_coach_id(self, coach_id: UUID) -> List[TrainingPlan]:
        """Get all training plans created by a coach."""
        response = self.table.scan(
            FilterExpression=Attr('coach_id').eq(str(coach_id)) & 
                           Attr('entity_type').eq('training_plan')
        )
        items = response.get('Items', [])
        return [self._item_to_plan(item) for item in items]
    
    async def get_by_customer_id(self, customer_id: UUID) -> List[TrainingPlan]:
        """Get all training plans assigned to a customer."""
        response = self.table.scan(
            FilterExpression=Attr('customer_id').eq(str(customer_id)) & 
                           Attr('entity_type').eq('training_plan')
        )
        items = response.get('Items', [])
        return [self._item_to_plan(item) for item in items]
    
    async def add_training_day(self, training_day: TrainingDay) -> TrainingDay:
        """Add a training day to a plan."""
        item = self._day_to_item(training_day)
        self.table.put_item(Item=item)
        return training_day
    
    async def update_training_day(self, training_day: TrainingDay) -> TrainingDay:
        """Update a training day."""
        training_day.updated_at = datetime.utcnow()
        item = self._day_to_item(training_day)
        self.table.put_item(Item=item)
        return training_day
    
    async def delete_training_day(self, training_day_id: UUID) -> bool:
        """Delete a training day."""
        # Need to find the training day first to get its pk and sk
        # This is a limitation - would need a GSI or different design
        # For now, simplified implementation
        raise NotImplementedError("Delete training day needs GSI or pk/sk lookup")
    
    async def get_training_days(self, plan_id: UUID) -> List[TrainingDay]:
        """Get all training days for a plan."""
        response = self.table.query(
            KeyConditionExpression=Key('pk').eq(f"PLAN#{str(plan_id)}") & 
                                 Key('sk').begins_with('DAY#')
        )
        items = response.get('Items', [])
        return sorted(
            [self._item_to_day(item) for item in items],
            key=lambda day: (day.date, day.day_order)
        )
