# GitHub Copilot Instructions

This document contains project-wide instructions for GitHub Copilot to help maintain code quality and consistency across the servidor backend project.

## Project Overview

This is a Python backend application following **Clean Architecture** principles with:
- **FastAPI** for REST API endpoints
- **DynamoDB & S3** for data storage (via LocalStack locally)
- **JWT + OAuth2** for authentication
- **Dependency Injection** for loose coupling
- **Multiple deployment targets**: ASGI (local/container) and AWS Lambda

## Architecture Principles

### Clean Architecture Layers

Follow the strict dependency rule: **dependencies only point inward**.

1. **Domain Layer** (`src/domain/`): Pure business logic
   - Contains entities and repository interfaces
   - No dependencies on frameworks or external services
   - Should be framework-agnostic and highly testable

2. **Application Layer** (`src/application/`): Use cases and workflows
   - Orchestrates business logic
   - Depends only on domain layer
   - Uses repository interfaces (not implementations)

3. **Infrastructure Layer** (`src/infrastructure/`): External services
   - Implements repository interfaces
   - Contains AWS clients, auth services, configuration
   - Can depend on domain and application layers

4. **Presentation Layer** (`src/presentation/`): API interface
   - HTTP endpoints and request/response handling
   - Uses application layer via dependency injection
   - No business logic

### Key Architectural Rules

- **Never import from outer layers into inner layers**
- Domain layer must remain pure (no FastAPI, boto3, etc.)
- Use dependency injection for all cross-layer dependencies
- Repository implementations belong in infrastructure, interfaces in domain
- Business rules live in entities and use cases, not controllers

## Code Organization

### File Structure
- Entity files: `src/domain/entities/*.py`
- Repository interfaces: `src/domain/repositories/*.py`
- Use cases: `src/application/use_cases/*.py`
- DTOs: `src/application/dtos/*.py`
- Repository implementations: `src/infrastructure/persistence/*.py`
- API routes: `src/presentation/api/v1/*.py`
- Schemas: `src/presentation/schemas/*.py`

### Naming Conventions
- Entities: `User`, `Task` (singular nouns)
- Repositories: `UserRepository`, `TaskRepository`
- Use cases: `AuthenticationUseCase`, `TaskUseCase`
- DTOs: `UserDTO`, `CreateUserDTO`, `UpdateTaskDTO`
- Schemas: `UserResponse`, `TaskCreate`, `TaskUpdate`

## Development Guidelines

### Adding New Features

When adding a new feature:
1. Start with the domain layer (entity + repository interface)
2. Create DTOs in application layer
3. Implement use case in application layer
4. Implement repository in infrastructure layer
5. Add API routes in presentation layer
6. Wire dependencies in `container.py`

### Testing Strategy

- **Unit tests**: Domain entities and use cases (mock repositories)
- **Integration tests**: API endpoints with real DynamoDB (LocalStack)
- Test files go in `tests/` directory
- Use `pytest` and `pytest-asyncio`
- Mock external services (AWS, databases) for unit tests

### Security Considerations

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs using Pydantic schemas
- Use JWT for authentication (configured in infrastructure)
- Follow principle of least privilege for AWS permissions

## Additional Instructions

For language-specific guidelines, refer to:
- [Python Guidelines](./.github/instructions/python.instructions.md)
- [Testing Guidelines](./.github/instructions/testing.instructions.md)
- [Security Guidelines](./.github/instructions/security.instructions.md)
- [Code Review Standards](./.github/instructions/code-review.instructions.md)
