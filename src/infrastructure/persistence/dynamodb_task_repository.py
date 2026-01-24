from typing import Optional, List
from uuid import UUID
from datetime import datetime
from boto3.dynamodb.conditions import Key
from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository
from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings


class DynamoDBTaskRepository(TaskRepository):
    """DynamoDB implementation of TaskRepository."""
    
    def __init__(self):
        self.dynamodb = AWSClientFactory.create_dynamodb_resource()
        self.table = self.dynamodb.Table(settings.dynamodb_tasks_table)
    
    def _to_item(self, task: Task) -> dict:
        """Convert Task entity to DynamoDB item."""
        return {
            'id': str(task.id),
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'user_id': str(task.user_id),
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        }
    
    def _from_item(self, item: dict) -> Task:
        """Convert DynamoDB item to Task entity."""
        task = Task(
            title=item['title'],
            description=item.get('description'),
            completed=item.get('completed', False),
            user_id=UUID(item['user_id']),
            id=UUID(item['id'])
        )
        task.created_at = datetime.fromisoformat(item['created_at'])
        task.updated_at = datetime.fromisoformat(item['updated_at'])
        return task
    
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        item = self._to_item(task)
        self.table.put_item(Item=item)
        return task
    
    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID."""
        response = self.table.get_item(Key={'id': str(task_id)})
        item = response.get('Item')
        return self._from_item(item) if item else None
    
    async def get_by_user_id(self, user_id: UUID) -> List[Task]:
        """Get all tasks for a user."""
        response = self.table.query(
            IndexName='user_id-index',
            KeyConditionExpression=Key('user_id').eq(str(user_id))
        )
        items = response.get('Items', [])
        return [self._from_item(item) for item in items]
    
    async def update(self, task: Task) -> Task:
        """Update existing task."""
        task.updated_at = datetime.utcnow()
        item = self._to_item(task)
        self.table.put_item(Item=item)
        return task
    
    async def delete(self, task_id: UUID) -> bool:
        """Delete task by ID."""
        self.table.delete_item(Key={'id': str(task_id)})
        return True
