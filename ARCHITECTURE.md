# Architecture Overview

## Clean Architecture Implementation

This project follows Uncle Bob's Clean Architecture principles with clear separation of concerns across 4 layers.

### Layer Dependencies

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                  │
│  (API Routes, Schemas, Middleware, Dependencies)│
│                     ↓                            │
│            Application Layer                     │
│      (Use Cases, DTOs, Services)                │
│                     ↓                            │
│             Domain Layer                         │
│      (Entities, Repository Interfaces)          │
└─────────────────────────────────────────────────┘
                       ↑
                       │
         ┌─────────────┴─────────────┐
         │   Infrastructure Layer     │
         │ (Persistence, AWS, Auth)   │
         └───────────────────────────┘
```

**Key Rule**: Dependencies point inward. Inner layers never depend on outer layers.

## Layer Details

### 1. Domain Layer (Enterprise Business Rules)
**Location**: `src/domain/`
**Responsibility**: Core business logic and rules
**Dependencies**: None (pure Python)

#### Components:
- **Entities** (`entities/`): Core business objects
  - `User`: User domain entity with business rules
  - `Task`: Task domain entity with state management
  - `Entity`: Base class for all entities

- **Repository Interfaces** (`repositories/`): Data access contracts
  - `UserRepository`: Interface for user data operations
  - `TaskRepository`: Interface for task data operations

**Principles**:
- No framework dependencies
- Pure business logic
- Framework-agnostic
- Highly testable

### 2. Application Layer (Application Business Rules)
**Location**: `src/application/`
**Responsibility**: Orchestrate business workflows
**Dependencies**: Domain layer only

#### Components:
- **Use Cases** (`use_cases/`): Business workflows
  - `AuthenticationUseCase`: User registration, login, token validation
  - `TaskUseCase`: CRUD operations for tasks

- **DTOs** (`dtos/`): Data transfer between layers
  - `UserDTO`, `CreateUserDTO`, `LoginDTO`, `TokenDTO`
  - `TaskDTO`, `CreateTaskDTO`, `UpdateTaskDTO`

**Principles**:
- No infrastructure dependencies
- Implements business workflows
- Uses repository interfaces (not implementations)

### 3. Infrastructure Layer (Frameworks & Drivers)
**Location**: `src/infrastructure/`
**Responsibility**: External services and frameworks
**Dependencies**: Domain and Application layers

#### Components:
- **Persistence** (`persistence/`): Repository implementations
  - `DynamoDBUserRepository`: User data in DynamoDB
  - `DynamoDBTaskRepository`: Task data in DynamoDB

- **AWS** (`aws/`): AWS service integration
  - `AWSClientFactory`: Create boto3 clients
  - `initializer`: Setup LocalStack resources

- **Auth** (`auth/`): Authentication services
  - `AuthService`: JWT token creation/validation, password hashing

- **Config** (`config/`): Application configuration
  - `settings`: Environment-based configuration
  - `logging`: Logging setup

- **Container** (`container.py`): Dependency injection
  - Wires all dependencies together
  - Provides service instances

**Principles**:
- Implements repository interfaces
- Handles external dependencies
- Can be swapped without touching business logic

### 4. Presentation Layer (Interface Adapters)
**Location**: `src/presentation/`
**Responsibility**: HTTP API and request/response handling
**Dependencies**: Application layer (via dependency injection)

#### Components:
- **API Routes** (`api/v1/`): HTTP endpoints
  - `auth.py`: Registration, login, user info
  - `tasks.py`: Task CRUD endpoints

- **Schemas** (`schemas/`): Request/response validation
  - Pydantic models for API contracts
  - Validation rules

- **Dependencies** (`api/dependencies.py`): FastAPI dependencies
  - `get_current_user`: Extract user from JWT
  - `get_current_active_user`: Verify user is active

- **Middleware** (`middleware/`): HTTP middleware
  - Error handling
  - Request logging

- **App Factory** (`api/app.py`): FastAPI application
  - Configure routes
  - Setup middleware
  - Wire dependencies

**Principles**:
- No business logic
- Translates HTTP to use cases
- Handles serialization/deserialization

## Entrypoints

### ASGI Entrypoint
**File**: `entrypoints/asgi.py`
**Use Case**: Local development, Docker, Kubernetes

```python
from src.presentation.api.app import create_app
app = create_app()
```

Run with: `uvicorn entrypoints.asgi:app --reload`

### Lambda Entrypoint
**File**: `entrypoints/lambda_handler.py`
**Use Case**: AWS Lambda deployment

```python
from mangum import Mangum
from src.presentation.api.app import create_app

app = create_app()
handler = Mangum(app, lifespan="off")
```

Deploy as: `entrypoints.lambda_handler.handler`

## Data Flow Example

### Creating a Task

1. **HTTP Request** → `POST /api/v1/tasks`
   ```json
   {"title": "Buy milk", "description": "From store"}
   ```

2. **Presentation Layer** (`tasks.py`)
   - Validates JWT token
   - Extracts current user
   - Validates request schema
   - Converts to `CreateTaskDTO`

3. **Application Layer** (`TaskUseCase`)
   - Receives DTO and user_id
   - Creates `Task` entity
   - Calls repository interface

4. **Infrastructure Layer** (`DynamoDBTaskRepository`)
   - Converts entity to DynamoDB item
   - Persists to DynamoDB
   - Returns entity

5. **Response** ← `TaskResponse` (201 Created)
   ```json
   {
     "id": "uuid",
     "title": "Buy milk",
     "completed": false,
     "user_id": "uuid"
   }
   ```

## Dependency Injection

Using `dependency-injector` for IoC:

```python
# Container definition
class Container(containers.DeclarativeContainer):
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
```

Injected into FastAPI routes:

```python
@router.post("/tasks")
@inject
async def create_task(
    task_data: TaskCreate,
    current_user: UserDTO = Depends(get_current_active_user),
    task_use_case: TaskUseCase = Depends(Provide[Container.task_use_case])
):
    # Use case is automatically injected
    return await task_use_case.create_task(dto, current_user.id)
```

## Testing Strategy

### Unit Tests
- **Domain Entities**: Test business rules in isolation
- **Use Cases**: Mock repositories, test workflows
- **Services**: Test individual service logic

### Integration Tests
- **Repository Implementations**: Test with real DynamoDB (LocalStack)
- **API Endpoints**: Test full request/response cycle

### Example
```python
@pytest.mark.asyncio
async def test_create_task():
    # Mock repository
    mock_repo = Mock(spec=TaskRepository)
    use_case = TaskUseCase(mock_repo)
    
    # Test use case
    dto = CreateTaskDTO(title="Test", description="Desc")
    result = await use_case.create_task(dto, user_id)
    
    assert result.title == "Test"
    mock_repo.create.assert_called_once()
```

## Benefits of This Architecture

1. **Testability**: Business logic is easy to test without external dependencies
2. **Flexibility**: Change databases, frameworks without touching business rules
3. **Maintainability**: Clear boundaries make code easier to understand
4. **Scalability**: Can add features without breaking existing code
5. **Independence**: Domain logic isn't coupled to frameworks

## Adding New Features

### To add a new entity (e.g., "Project"):

1. **Domain**: Create `Project` entity and `ProjectRepository` interface
2. **Application**: Create `ProjectDTO` and `ProjectUseCase`
3. **Infrastructure**: Implement `DynamoDBProjectRepository`
4. **Presentation**: Create `project.py` routes and schemas
5. **Container**: Wire up dependencies

Each layer changes independently, following the Dependency Rule.
