import boto3
from typing import Optional
from src.infrastructure.config.settings import settings


class AWSClientFactory:
    """Factory for creating AWS service clients."""
    
    @staticmethod
    def _get_client_config() -> dict:
        """Get common configuration for AWS clients."""
        config = {
            'region_name': settings.aws_region,
            'aws_access_key_id': settings.aws_access_key_id,
            'aws_secret_access_key': settings.aws_secret_access_key,
        }
        
        if settings.environment == 'local':
            config['endpoint_url'] = settings.aws_endpoint_url
        
        return config
    
    @staticmethod
    def create_dynamodb_client():
        """Create DynamoDB client."""
        return boto3.client('dynamodb', **AWSClientFactory._get_client_config())
    
    @staticmethod
    def create_dynamodb_resource():
        """Create DynamoDB resource."""
        return boto3.resource('dynamodb', **AWSClientFactory._get_client_config())
    
    @staticmethod
    def create_s3_client():
        """Create S3 client."""
        return boto3.client('s3', **AWSClientFactory._get_client_config())
