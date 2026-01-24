# Quick Start Guide

## Start the Application

```bash
# Option 1: Using Docker Compose (Recommended)
docker-compose up --build

# Option 2: Local Development
make localstack  # In one terminal
make run         # In another terminal
```

## Test the API

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"
```

Save the token from response!

### 4. Create Task
```bash
TOKEN="your_token_here"
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "My Task",
    "description": "Task description"
  }'
```

### 5. List Tasks
```bash
curl -X GET http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer $TOKEN"
```

## Interactive API Documentation

Visit: http://localhost:8000/docs

## Project Structure

```
src/
├── domain/              # Pure business logic (no dependencies)
│   ├── entities/        # User, Task
│   └── repositories/    # Repository interfaces
├── application/         # Use cases (business workflows)
│   ├── use_cases/       # AuthenticationUseCase, TaskUseCase
│   └── dtos/            # Data Transfer Objects
├── infrastructure/      # External services
│   ├── persistence/     # DynamoDB implementations
│   ├── aws/             # AWS clients
│   ├── auth/            # JWT service
│   └── container.py     # Dependency injection
└── presentation/        # API layer
    ├── api/v1/          # Route handlers
    ├── schemas/         # Request/response models
    └── middleware/      # Error handling, etc.
```

## Available Commands

```bash
make help          # Show all commands
make install       # Install dependencies
make run           # Run locally
make test          # Run tests
make docker-up     # Start with Docker
make docker-down   # Stop Docker
make clean         # Clean cache files
```

## Architecture Principles

1. **Dependency Inversion**: Inner layers don't depend on outer layers
2. **Single Responsibility**: Each class has one reason to change
3. **Interface Segregation**: Use specific interfaces, not general ones
4. **Open/Closed**: Open for extension, closed for modification

## Next Steps

1. Add more domain entities and use cases
2. Implement additional repositories
3. Add more comprehensive tests
4. Configure CI/CD pipeline
5. Deploy to AWS Lambda
