from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import json


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from .env
    )
    
    # Application
    app_name: str = Field(default="servidor", alias="APP_NAME")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Security
    secret_key: str = Field(default="secret-key-change-in-production", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # AWS
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    aws_access_key_id: str = Field(default="test", alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(default="test", alias="AWS_SECRET_ACCESS_KEY")
    aws_endpoint_url: str = Field(default="http://localhost:4566", alias="AWS_ENDPOINT_URL")
    
    # DynamoDB
    dynamodb_users_table: str = Field(default="users", alias="DYNAMODB_USERS_TABLE")
    dynamodb_training_plans_table: str = Field(default="training_plans", alias="DYNAMODB_TRAINING_PLANS_TABLE")
    dynamodb_activities_table: str = Field(default="strava_activities", alias="DYNAMODB_ACTIVITIES_TABLE")
    
    # S3
    s3_bucket_name: str = Field(default="servidor-files", alias="S3_BUCKET_NAME")
    
    # Strava
    strava_client_id: str = Field(default="", alias="STRAVA_CLIENT_ID")
    strava_client_secret: str = Field(default="", alias="STRAVA_CLIENT_SECRET")
    strava_webhook_verify_token: str = Field(default="STRAVA_WEBHOOK_SECRET", alias="STRAVA_WEBHOOK_VERIFY_TOKEN")
    strava_callback_url: str = Field(default="http://localhost:8000/api/v1/strava/callback", alias="STRAVA_CALLBACK_URL")
    
    # API
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    cors_origins: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        alias="CORS_ORIGINS"
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from JSON string or return as-is if already a list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v


settings = Settings()
