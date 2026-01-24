"""
DynamoDB Activity Repository implementation.
"""
import json
from datetime import datetime
from typing import List, Optional
from uuid import UUID

import boto3
from boto3.dynamodb.conditions import Key, Attr

from src.domain.repositories.activity_repository import ActivityRepository
from src.domain.entities.strava_activity import StravaActivity
from src.domain.entities.enums import ActivityMatchStatus


class DynamoDBActivityRepository(ActivityRepository):
    """DynamoDB implementation of Activity repository."""
    
    def __init__(self, dynamodb_endpoint: str, table_name: str, region: str = "us-east-1"):
        """
        Initialize repository.
        
        Args:
            dynamodb_endpoint: DynamoDB endpoint URL
            table_name: Name of activities table
            region: AWS region
        """
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=dynamodb_endpoint,
            region_name=region
        )
        self.table = self.dynamodb.Table(table_name)
    
    def _to_item(self, activity: StravaActivity) -> dict:
        """Convert activity entity to DynamoDB item."""
        item = {
            'PK': f"CUSTOMER#{str(activity.customer_id)}",
            'SK': f"ACTIVITY#{activity.strava_activity_id}#{activity.start_date.isoformat()}",
            'id': str(activity.id),
            'customer_id': str(activity.customer_id),
            'strava_activity_id': activity.strava_activity_id,
            'name': activity.name,
            'activity_type': activity.activity_type,
            'start_date': activity.start_date.isoformat(),
            'distance': str(activity.distance),
            'moving_time': activity.moving_time,
            'elapsed_time': activity.elapsed_time,
            'match_status': activity.match_status.value,
            'kudos_count': activity.kudos_count,
            'comment_count': activity.comment_count,
            'achievement_count': activity.achievement_count,
            'created_at': activity.created_at.isoformat(),
        }
        
        # Optional fields
        if activity.total_elevation_gain is not None:
            item['total_elevation_gain'] = str(activity.total_elevation_gain)
        if activity.average_speed is not None:
            item['average_speed'] = str(activity.average_speed)
        if activity.max_speed is not None:
            item['max_speed'] = str(activity.max_speed)
        if activity.average_pace is not None:
            item['average_pace'] = str(activity.average_pace)
        if activity.average_heartrate is not None:
            item['average_heartrate'] = str(activity.average_heartrate)
        if activity.max_heartrate is not None:
            item['max_heartrate'] = str(activity.max_heartrate)
        if activity.calories is not None:
            item['calories'] = str(activity.calories)
        if activity.suffer_score is not None:
            item['suffer_score'] = str(activity.suffer_score)
        if activity.heartrate_zones:
            item['heartrate_zones'] = json.dumps(activity.heartrate_zones)
        if activity.splits:
            item['splits'] = json.dumps(activity.splits)
        if activity.laps:
            item['laps'] = json.dumps(activity.laps)
        if activity.photos:
            item['photos'] = json.dumps(activity.photos)
        if activity.map_polyline:
            item['map_polyline'] = activity.map_polyline
        if activity.training_day_id:
            item['training_day_id'] = str(activity.training_day_id)
        
        return item
    
    def _from_item(self, item: dict) -> StravaActivity:
        """Convert DynamoDB item to activity entity."""
        return StravaActivity(
            id=UUID(item['id']),
            customer_id=UUID(item['customer_id']),
            strava_activity_id=int(item['strava_activity_id']),
            name=item['name'],
            activity_type=item['activity_type'],
            start_date=datetime.fromisoformat(item['start_date']),
            distance=float(item['distance']),
            moving_time=int(item['moving_time']),
            elapsed_time=int(item['elapsed_time']),
            total_elevation_gain=float(item['total_elevation_gain']) if 'total_elevation_gain' in item else None,
            average_speed=float(item['average_speed']) if 'average_speed' in item else None,
            max_speed=float(item['max_speed']) if 'max_speed' in item else None,
            average_pace=float(item['average_pace']) if 'average_pace' in item else None,
            average_heartrate=float(item['average_heartrate']) if 'average_heartrate' in item else None,
            max_heartrate=float(item['max_heartrate']) if 'max_heartrate' in item else None,
            heartrate_zones=json.loads(item['heartrate_zones']) if 'heartrate_zones' in item else None,
            splits=json.loads(item['splits']) if 'splits' in item else None,
            laps=json.loads(item['laps']) if 'laps' in item else None,
            calories=float(item['calories']) if 'calories' in item else None,
            suffer_score=float(item['suffer_score']) if 'suffer_score' in item else None,
            kudos_count=int(item.get('kudos_count', 0)),
            comment_count=int(item.get('comment_count', 0)),
            achievement_count=int(item.get('achievement_count', 0)),
            photos=json.loads(item['photos']) if 'photos' in item else None,
            map_polyline=item.get('map_polyline'),
            training_day_id=UUID(item['training_day_id']) if 'training_day_id' in item else None,
            match_status=ActivityMatchStatus(item['match_status']),
            created_at=datetime.fromisoformat(item['created_at'])
        )
    
    async def create(self, activity: StravaActivity) -> StravaActivity:
        """Create a new activity."""
        item = self._to_item(activity)
        self.table.put_item(Item=item)
        return activity
    
    async def get_by_id(self, activity_id: UUID) -> Optional[StravaActivity]:
        """Get activity by ID using scan (inefficient, consider GSI)."""
        response = self.table.scan(
            FilterExpression=Attr('id').eq(str(activity_id))
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def get_by_strava_id(
        self,
        strava_activity_id: int,
        customer_id: UUID
    ) -> Optional[StravaActivity]:
        """Get activity by Strava ID and customer."""
        # Query by PK and filter by strava_activity_id
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f"CUSTOMER#{str(customer_id)}") &
                                 Key('SK').begins_with(f"ACTIVITY#{strava_activity_id}#")
        )
        items = response.get('Items', [])
        return self._from_item(items[0]) if items else None
    
    async def get_by_customer(
        self,
        customer_id: UUID,
        limit: int = 100
    ) -> List[StravaActivity]:
        """Get all activities for a customer."""
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f"CUSTOMER#{str(customer_id)}") &
                                 Key('SK').begins_with('ACTIVITY#'),
            Limit=limit,
            ScanIndexForward=False  # Newest first
        )
        return [self._from_item(item) for item in response.get('Items', [])]
    
    async def get_by_date_range(
        self,
        customer_id: UUID,
        start_date: datetime,
        end_date: datetime
    ) -> List[StravaActivity]:
        """Get activities within a date range."""
        # Get all customer activities and filter by date
        all_activities = await self.get_by_customer(customer_id, limit=1000)
        return [
            activity for activity in all_activities
            if start_date <= activity.start_date <= end_date
        ]
    
    async def get_unmatched_activities(
        self,
        customer_id: UUID
    ) -> List[StravaActivity]:
        """Get all unmatched activities for a customer."""
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f"CUSTOMER#{str(customer_id)}") &
                                 Key('SK').begins_with('ACTIVITY#'),
            FilterExpression=Attr('match_status').eq(ActivityMatchStatus.UNMATCHED.value)
        )
        return [self._from_item(item) for item in response.get('Items', [])]
    
    async def update(self, activity: StravaActivity) -> StravaActivity:
        """Update an existing activity."""
        item = self._to_item(activity)
        self.table.put_item(Item=item)
        return activity
    
    async def update_match_status(
        self,
        activity_id: UUID,
        training_day_id: Optional[UUID],
        match_status: ActivityMatchStatus
    ) -> None:
        """Update activity matching status."""
        activity = await self.get_by_id(activity_id)
        if not activity:
            raise ValueError("Activity not found")
        
        activity.training_day_id = training_day_id
        activity.match_status = match_status
        await self.update(activity)
    
    async def delete(self, activity_id: UUID) -> bool:
        """Delete an activity."""
        activity = await self.get_by_id(activity_id)
        if not activity:
            return False
        
        self.table.delete_item(
            Key={
                'PK': f"CUSTOMER#{str(activity.customer_id)}",
                'SK': f"ACTIVITY#{activity.strava_activity_id}#{activity.start_date.isoformat()}"
            }
        )
        return True
