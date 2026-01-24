from .dynamodb_user_repository import DynamoDBUserRepository
from .dynamodb_coach_repository import DynamoDBCoachRepository
from .dynamodb_customer_repository import DynamoDBCustomerRepository
from .dynamodb_training_plan_repository import DynamoDBTrainingPlanRepository
from .dynamodb_activity_repository import DynamoDBActivityRepository
from .dynamodb_admin_repository import DynamoDBAdminRepository

__all__ = [
    "DynamoDBUserRepository",
    "DynamoDBCoachRepository",
    "DynamoDBCustomerRepository",
    "DynamoDBTrainingPlanRepository",
    "DynamoDBActivityRepository",
    "DynamoDBAdminRepository"
]
