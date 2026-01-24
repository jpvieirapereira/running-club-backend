from dependency_injector import containers, providers
from src.infrastructure.persistence import DynamoDBUserRepository, DynamoDBTaskRepository
from src.infrastructure.auth import AuthService
from src.application.use_cases import AuthenticationUseCase, TaskUseCase


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.api.v1.auth",
            "src.presentation.api.v1.tasks",
            "src.presentation.api.dependencies",
        ]
    )
    
    # Infrastructure
    auth_service = providers.Singleton(AuthService)
    
    # Repositories
    user_repository = providers.Factory(DynamoDBUserRepository)
    task_repository = providers.Factory(DynamoDBTaskRepository)
    
    # Use Cases
    authentication_use_case = providers.Factory(
        AuthenticationUseCase,
        user_repository=user_repository,
        auth_service=auth_service
    )
    
    task_use_case = providers.Factory(
        TaskUseCase,
        task_repository=task_repository
    )
