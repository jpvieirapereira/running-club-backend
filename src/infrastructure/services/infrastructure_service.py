"""
Infrastructure service for creating AWS resources.
"""
import boto3
from typing import Dict, Any, List

from src.infrastructure.config import settings


class InfrastructureService:
    """Service for creating and managing AWS infrastructure."""
    
    def __init__(self):
        """Initialize infrastructure service."""
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
        self.s3 = boto3.client(
            's3',
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
    
    def create_dynamodb_tables(self) -> Dict[str, Any]:
        """
        Create all DynamoDB tables required by the application.
        
        Returns:
            Dictionary with creation status for each table
        """
        results = {}
        
        # Users table
        results['users'] = self._create_users_table()
        
        # Training plans table
        results['training_plans'] = self._create_training_plans_table()
        
        # Strava activities table
        results['strava_activities'] = self._create_activities_table()
        
        return results
    
    def _create_users_table(self) -> str:
        """Create users table with email GSI."""
        try:
            table = self.dynamodb.create_table(
                TableName=settings.dynamodb_users_table,
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'email', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'email-index',
                        'KeySchema': [
                            {'AttributeName': 'email', 'KeyType': 'HASH'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                BillingMode='PROVISIONED',
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            return f"Created: {settings.dynamodb_users_table}"
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            return f"Already exists: {settings.dynamodb_users_table}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _create_training_plans_table(self) -> str:
        """Create training plans table with composite key."""
        try:
            table = self.dynamodb.create_table(
                TableName=settings.dynamodb_training_plans_table,
                KeySchema=[
                    {'AttributeName': 'PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'SK', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'PK', 'AttributeType': 'S'},
                    {'AttributeName': 'SK', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
            return f"Created: {settings.dynamodb_training_plans_table}"
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            return f"Already exists: {settings.dynamodb_training_plans_table}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _create_activities_table(self) -> str:
        """Create Strava activities table with composite key."""
        try:
            table = self.dynamodb.create_table(
                TableName=settings.dynamodb_activities_table,
                KeySchema=[
                    {'AttributeName': 'PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'SK', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'PK', 'AttributeType': 'S'},
                    {'AttributeName': 'SK', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
            return f"Created: {settings.dynamodb_activities_table}"
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            return f"Already exists: {settings.dynamodb_activities_table}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def create_s3_buckets(self) -> Dict[str, Any]:
        """
        Create all S3 buckets required by the application.
        
        Returns:
            Dictionary with creation status for each bucket
        """
        results = {}
        
        try:
            self.s3.create_bucket(Bucket=settings.s3_bucket_name)
            results[settings.s3_bucket_name] = f"Created: {settings.s3_bucket_name}"
        except self.s3.exceptions.BucketAlreadyOwnedByYou:
            results[settings.s3_bucket_name] = f"Already exists: {settings.s3_bucket_name}"
        except self.s3.exceptions.BucketAlreadyExists:
            results[settings.s3_bucket_name] = f"Already exists (different owner): {settings.s3_bucket_name}"
        except Exception as e:
            results[settings.s3_bucket_name] = f"Error: {str(e)}"
        
        return results
    
    def list_tables(self) -> List[str]:
        """List all DynamoDB tables."""
        client = self.dynamodb.meta.client
        return client.list_tables()['TableNames']
    
    def list_buckets(self) -> List[str]:
        """List all S3 buckets."""
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]
