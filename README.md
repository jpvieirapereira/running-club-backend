# Servidor - Clean Architecture Backend

A Python backend following Clean Architecture principles with FastAPI, supporting both Lambda and ASGI deployments.

## Architecture

```
servidor/
├── src/
│   ├── domain/              # Enterprise Business Rules
│   │   ├── entities/        # Domain entities
│   │   └── repositories/    # Repository interfaces
│   ├── application/         # Application Business Rules
│   │   ├── use_cases/       # Use case implementations
│   │   └── dtos/            # Data Transfer Objects
│   ├── infrastructure/      # Frameworks & Drivers
│   │   ├── persistence/     # Repository implementations
│   │   ├── aws/             # AWS service clients
│   │   ├── auth/            # Authentication service
│   │   ├── config/          # Configuration
│   │   └── container.py     # Dependency Injection
│   └── presentation/        # Interface Adapters
│       ├── api/             # API routes and controllers
│       ├── schemas/         # Request/Response schemas
│       └── middleware/      # HTTP middleware
├── entrypoints/
│   ├── asgi.py             # ASGI entrypoint (local/container)
│   └── lambda_handler.py   # Lambda entrypoint (AWS)
└── tests/                  # Test suite
```

## Features

- ✅ **Clean Architecture**: Clear separation of concerns with dependency inversion
- ✅ **FastAPI**: Modern, fast web framework with automatic OpenAPI docs
- ✅ **Swagger/OpenAPI**: Interactive API documentation at `/docs`
- ✅ **Multiple Entrypoints**: ASGI for local development, Lambda handler for AWS
- ✅ **Dependency Injection**: Using `dependency-injector` for IoC
- ✅ **JWT + OAuth2**: Secure authentication with password flow
- ✅ **DynamoDB + S3**: AWS services simulated with LocalStack
- ✅ **UV Package Manager**: Fast Python package management
- ✅ **Docker Compose**: Local development environment

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- UV package manager (or pip)

## Quick Start

### 1. Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
cd servidor
cp .env.example .env
```

### 3. Install Dependencies

```bash
uv pip install -r pyproject.toml
```

### 4. Run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **LocalStack**: http://localhost:4566

## Development

### Run Locally (without Docker)

1. Start LocalStack:
```bash
docker-compose up localstack
```

2. Run the API:
```bash
uvicorn entrypoints.asgi:app --reload
```

### Run Tests

```bash
pytest
```

### Code Structure

#### Domain Layer
- **Entities**: Core business objects (User, Task)
- **Repositories**: Interfaces for data access
- No external dependencies

#### Application Layer
- **Use Cases**: Business logic orchestration
- **DTOs**: Data transfer between layers
- Depends only on domain layer

#### Infrastructure Layer
- **Persistence**: DynamoDB repository implementations
- **AWS**: Service clients and initializers
- **Auth**: JWT token service and password hashing
- **Container**: Dependency injection setup

#### Presentation Layer
- **API Routes**: HTTP endpoints
- **Schemas**: Pydantic models for validation
- **Dependencies**: FastAPI dependencies (auth, etc.)
- **Middleware**: Error handling, CORS

## API Usage

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

Or use JSON:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### 3. Create a Task (Authenticated)

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "My First Task",
    "description": "Task description"
  }'
```

### 4. List Tasks

```bash
curl -X GET http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Update Task

```bash
curl -X PUT http://localhost:8000/api/v1/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Updated Title",
    "completed": true
  }'
```

## AWS Lambda Deployment

The application supports AWS Lambda deployment using the Mangum adapter.

### Lambda Configuration

- **Handler**: `entrypoints.lambda_handler.handler`
- **Runtime**: Python 3.11
- **Environment Variables**: Set from `.env.example`

### Deployment Options

1. **AWS SAM**:
```yaml
Resources:
  ServerFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: entrypoints.lambda_handler.handler
      Runtime: python3.11
      Environment:
        Variables:
          AWS_ENDPOINT_URL: ""  # Empty for production
```

2. **Serverless Framework**:
```yaml
functions:
  api:
    handler: entrypoints.lambda_handler.handler
    runtime: python3.11
    events:
      - http: ANY /
      - http: ANY /{proxy+}
```

3. **AWS CDK**:
```python
lambda_function = aws_lambda.Function(
    self, "ServerFunction",
    runtime=aws_lambda.Runtime.PYTHON_3_11,
    handler="entrypoints.lambda_handler.handler",
    code=aws_lambda.Code.from_asset(".")
)
```

## Environment Variables

See `.env.example` for all configuration options:

- **Application**: `APP_NAME`, `ENVIRONMENT`, `DEBUG`
- **Security**: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- **AWS**: `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- **DynamoDB**: `DYNAMODB_USERS_TABLE`, `DYNAMODB_TASKS_TABLE`
- **S3**: `S3_BUCKET_NAME`

## Clean Architecture Benefits

1. **Independence**: Business logic doesn't depend on frameworks
2. **Testability**: Easy to test use cases without external dependencies
3. **Flexibility**: Change infrastructure without touching business logic
4. **Maintainability**: Clear boundaries and responsibilities

## Contributing

1. Follow clean architecture principles
2. Keep domain layer pure (no external dependencies)
3. Use dependency injection for all services
4. Write tests for use cases
5. Update API documentation

## License

MIT
