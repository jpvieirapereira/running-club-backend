from dependency_injector import containers, providers
from src.infrastructure.persistence import (
    DynamoDBUserRepository,
    DynamoDBCoachRepository,
    DynamoDBCustomerRepository,
    DynamoDBTrainingPlanRepository,
    DynamoDBActivityRepository,
    DynamoDBAdminRepository
)
from src.infrastructure.auth import AuthService
from src.infrastructure.external import StravaAPIClient
from src.infrastructure.services import InfrastructureService
from src.infrastructure.config import settings
from src.application.use_cases import (
    AuthenticationUseCase,
    CoachUseCase,
    CustomerUseCase,
    TrainingPlanUseCase,
    StravaIntegrationUseCase,
    ActivitySyncUseCase,
    AdminUseCase
)


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.api.v1.auth",
            "src.presentation.api.v1.training_plans",
            "src.presentation.api.v1.strava",
            "src.presentation.api.v1.webhooks",
            "src.presentation.api.dependencies",
        ]
    )
    
    # Infrastructure
    auth_service = providers.Singleton(AuthService)
    
    strava_client = providers.Singleton(
        StravaAPIClient,
        client_id=settings.strava_client_id,
        client_secret=settings.strava_client_secret,
        webhook_verify_token=settings.strava_webhook_verify_token
    )
    
    infrastructure_service = providers.Singleton(InfrastructureService)
    
    # Repositories
    user_repository = providers.Factory(DynamoDBUserRepository)
    coach_repository = providers.Factory(DynamoDBCoachRepository)
    customer_repository = providers.Factory(DynamoDBCustomerRepository)
    admin_repository = providers.Factory(DynamoDBAdminRepository)
    training_plan_repository = providers.Factory(DynamoDBTrainingPlanRepository)
    activity_repository = providers.Factory(
        DynamoDBActivityRepository,
        dynamodb_endpoint=settings.aws_endpoint_url,
        table_name=settings.dynamodb_activities_table,
        region=settings.aws_region
    )
    
    # Use Cases
    authentication_use_case = providers.Factory(
        AuthenticationUseCase,
        coach_repository=coach_repository,
        customer_repository=customer_repository,
        auth_service=auth_service
    )
    
    coach_use_case = providers.Factory(
        CoachUseCase,
        coach_repository=coach_repository,
        customer_repository=customer_repository,
        auth_service=auth_service
    )
    
    customer_use_case = providers.Factory(
        CustomerUseCase,
        customer_repository=customer_repository,
        auth_service=auth_service
    )
    
    training_plan_use_case = providers.Factory(
        TrainingPlanUseCase,
        training_plan_repository=training_plan_repository,
        customer_repository=customer_repository
    )
    
    strava_integration_use_case = providers.Factory(
        StravaIntegrationUseCase,
        customer_repository=customer_repository,
        strava_client=strava_client
    )
    
    activity_sync_use_case = providers.Factory(
        ActivitySyncUseCase,
        activity_repository=activity_repository,
        customer_repository=customer_repository,
        training_plan_repository=training_plan_repository,
        strava_client=strava_client
    )
    
    admin_use_case = providers.Factory(
        AdminUseCase,
        admin_repository=admin_repository,
        auth_service=auth_service
    )


