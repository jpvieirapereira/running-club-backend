from src.infrastructure.aws.client_factory import AWSClientFactory
from src.infrastructure.config import settings, logger


async def initialize_aws_resources():
    """Initialize AWS resources (tables, buckets) for local development."""
    if settings.environment != 'local':
        logger.info("Skipping AWS resource initialization in non-local environment")
        return
    
    try:
        dynamodb = AWSClientFactory.create_dynamodb_resource()
        s3_client = AWSClientFactory.create_s3_client()
        
        # Create Users table
        try:
            dynamodb.create_table(
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
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            logger.info(f"Created DynamoDB table: {settings.dynamodb_users_table}")
        except dynamodb.meta.client.exceptions.ResourceInUseException:
            logger.info(f"Table {settings.dynamodb_users_table} already exists")
        
        # Create S3 bucket
        try:
            s3_client.create_bucket(Bucket=settings.s3_bucket_name)
            logger.info(f"Created S3 bucket: {settings.s3_bucket_name}")
        except s3_client.exceptions.BucketAlreadyOwnedByYou:
            logger.info(f"Bucket {settings.s3_bucket_name} already exists")
        except Exception as e:
            logger.warning(f"Could not create S3 bucket: {e}")
    
    except Exception as e:
        logger.error(f"Error initializing AWS resources: {e}")
