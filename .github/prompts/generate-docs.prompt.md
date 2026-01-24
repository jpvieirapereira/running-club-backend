---
agent: 'agent'
model: Claude Sonnet 4
tools: ['edit', 'create', 'codebase', 'search']
description: 'Generate or update project documentation'
---

# Generate Documentation

You are helping create and maintain documentation for the servidor backend project.

## Documentation Types

### 1. Code Documentation (Docstrings)

Generate Google-style docstrings for functions and classes:

```python
async def create_task(self, dto: CreateTaskDTO, user_id: UUID) -> TaskDTO:
    """
    Create a new task for a user.
    
    This method creates a new Task entity, assigns it to the specified user,
    and persists it to the database. The task will be initialized with
    completed=False.
    
    Args:
        dto: Data transfer object containing task details (title, description)
        user_id: UUID of the user who owns the task
    
    Returns:
        TaskDTO containing the created task data including generated ID
    
    Raises:
        ValueError: If title is empty or user_id is invalid
    
    Example:
        >>> dto = CreateTaskDTO(title="Buy milk", description="From store")
        >>> task = await use_case.create_task(dto, user_id)
        >>> print(task.title)
        'Buy milk'
    """
```

### 2. API Documentation

Generate OpenAPI documentation for endpoints:

```python
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="""
    Create a new task for the authenticated user.
    
    The task will be created with the provided title and description,
    and will be initialized with completed=False. The task ID will be
    automatically generated.
    
    Requires authentication via JWT token.
    """,
    responses={
        201: {
            "description": "Task created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Buy groceries",
                        "description": "Milk, bread, eggs",
                        "completed": False,
                        "user_id": "987fcdeb-51a2-43f7-8d9c-123456789abc"
                    }
                }
            }
        },
        400: {"description": "Invalid request data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"}
    },
    tags=["Tasks"]
)
```

### 3. README Documentation

#### Main README Structure

```markdown
# Project Name

Brief description of what the project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Architecture

Brief architecture overview with diagram if possible.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- UV package manager

## Quick Start

\`\`\`bash
# Clone and setup
git clone <repo>
cd proyecto
cp .env.example .env

# Run with Docker
docker-compose up --build

# Visit API
open http://localhost:8000/docs
\`\`\`

## Installation

Detailed installation instructions...

## Configuration

Environment variables and configuration options...

## API Documentation

Link to Swagger/ReDoc and examples...

## Testing

How to run tests...

## Deployment

Deployment instructions for different environments...

## Contributing

Contribution guidelines...

## License

License information...
```

### 4. Architecture Documentation

Generate ARCHITECTURE.md:

```markdown
# Architecture Overview

## Clean Architecture Layers

Description of each layer...

## Data Flow

Describe how data flows through the system...

## Design Decisions

Document important architecture decisions...

## Adding New Features

Step-by-step guide for adding features...
```

### 5. API Examples

Create comprehensive API usage examples:

```markdown
# API Examples

## Authentication

### Register User
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
\`\`\`

Response:
\`\`\`json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
\`\`\`

### Login
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/auth/login \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "username=user@example.com&password=SecurePass123!"
\`\`\`

Response:
\`\`\`json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
\`\`\`

## Tasks

### Create Task
\`\`\`bash
TOKEN="your_access_token"
curl -X POST http://localhost:8000/api/v1/tasks \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer $TOKEN" \\
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs"
  }'
\`\`\`
```

### 6. Configuration Documentation

Document environment variables:

```markdown
# Configuration

## Environment Variables

### Application Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_NAME` | string | `servidor` | Application name |
| `ENVIRONMENT` | string | `local` | Environment: local, staging, production |
| `DEBUG` | boolean | `true` | Enable debug mode |

### Security Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SECRET_KEY` | string | (required) | JWT secret key, min 32 characters |
| `ALGORITHM` | string | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | integer | `30` | Token expiration time |

### AWS Settings

...
```

### 7. Changelog

Maintain CHANGELOG.md:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Feature X implementation

### Changed
- Updated dependency Y

### Fixed
- Bug fix for Z

## [0.2.0] - 2024-01-20

### Added
- Task CRUD operations
- JWT authentication
- DynamoDB integration

### Changed
- Improved error handling
- Updated API documentation

### Fixed
- Token validation bug
- User creation edge case

## [0.1.0] - 2024-01-10

### Added
- Initial project structure
- Clean architecture setup
- FastAPI configuration
```

## Documentation Checklist

When generating documentation, ensure:

**Code Documentation:**
- [ ] All public functions have docstrings
- [ ] Parameters are documented
- [ ] Return types are documented
- [ ] Exceptions are documented
- [ ] Examples provided where helpful

**API Documentation:**
- [ ] All endpoints documented
- [ ] Request/response schemas defined
- [ ] Examples provided
- [ ] Error responses documented
- [ ] Authentication requirements clear

**README:**
- [ ] Up to date with current features
- [ ] Installation steps are clear
- [ ] Configuration options documented
- [ ] Examples work
- [ ] Links are valid

**Architecture Docs:**
- [ ] Reflects current architecture
- [ ] Design decisions explained
- [ ] Diagrams are current
- [ ] Adding features guide updated

**Changelog:**
- [ ] Recent changes documented
- [ ] Version numbers correct
- [ ] Links to issues/PRs included

## Process

1. **Analyze**: Review the code/feature to document
2. **Draft**: Create documentation following templates
3. **Review**: Check for accuracy and completeness
4. **Test**: Verify examples actually work
5. **Update**: Keep documentation in sync with code

Ask the user what documentation they need!
