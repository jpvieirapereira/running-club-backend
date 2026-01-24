---
description: 'Documentation standards for servidor backend'
applyTo: '**/*.py,**/*.md'
---

# Documentation Standards

## Code Documentation

### Docstrings (PEP 257)

All public modules, classes, functions, and methods must have docstrings.

**Format**: Use Google-style docstrings

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When input is invalid
        KeyError: When key is not found
    
    Example:
        >>> result = function_name("test", 123)
        >>> print(result)
        'processed: test-123'
    """
```

### Class Documentation

```python
class UserRepository:
    """
    Repository for managing User entities in DynamoDB.
    
    This repository implements the UserRepository interface and provides
    methods for CRUD operations on User entities. It handles conversion
    between domain entities and DynamoDB items.
    
    Attributes:
        table: DynamoDB table resource
        table_name: Name of the DynamoDB table
    """
```

### Module Documentation

Every Python module should have a module-level docstring:

```python
"""
User authentication and authorization use cases.

This module contains use cases related to user management,
including registration, login, and token validation.
"""
```

## API Documentation

### FastAPI Endpoints

Use FastAPI's built-in documentation features:

```python
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Not authenticated"}
    }
)
async def create_task(
    task_data: TaskCreate,
    current_user: UserDTO = Depends(get_current_active_user)
):
    """
    Create a new task.
    
    This endpoint creates a new task for the authenticated user.
    The task will be initialized with completed=False.
    """
```

### Pydantic Schemas

Document Pydantic models with Field descriptions:

```python
class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description", max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, bread, eggs"
            }
        }
```

## README Documentation

### Project README Structure

The main README.md should include:
1. Project title and brief description
2. Features list
3. Architecture overview
4. Prerequisites
5. Installation instructions
6. Usage examples
7. API documentation link
8. Configuration options
9. Testing instructions
10. Deployment guide
11. Contributing guidelines (if applicable)
12. License

### Component READMEs

For complex components, add a README.md in the directory:
- `src/domain/README.md` - Domain layer overview
- `src/infrastructure/README.md` - Infrastructure details

## Architecture Documentation

Maintain these documentation files:
- **ARCHITECTURE.md**: Detailed architecture explanation
- **QUICKSTART.md**: Quick start guide for developers
- **DEPLOYMENT.md**: Deployment procedures
- **CHANGELOG.md**: Version history and changes

## Inline Comments

### When to Comment

Comment on:
- Complex algorithms or business logic
- Non-obvious design decisions
- Workarounds for known issues
- Performance optimizations
- Security considerations

### When NOT to Comment

Don't comment on:
- Self-explanatory code
- What the code does (use descriptive names instead)
- Obvious operations

### Good Comments

```python
# Check ownership before deletion to prevent unauthorized access
if task.user_id != current_user.id:
    raise ValueError("Not authorized")

# Use GSI for efficient lookup by email
response = self.table.query(
    IndexName='email-index',
    KeyConditionExpression=Key('email').eq(email)
)
```

### Bad Comments

```python
# Loop through tasks
for task in tasks:
    # Print task
    print(task)

# Create user
user = User(...)
```

## Type Hints as Documentation

Use type hints to document expected types:

```python
from typing import Optional, List, Dict, Union
from uuid import UUID

async def get_tasks(
    user_id: UUID,
    completed: Optional[bool] = None,
    limit: int = 100
) -> List[Task]:
    """Get tasks for a user with optional filtering."""
```

## Environment Variables Documentation

Document all environment variables in `.env.example`:

```bash
# Application Settings
APP_NAME=servidor                    # Application name
ENVIRONMENT=local                    # Environment: local, staging, production
DEBUG=true                          # Enable debug mode (true/false)

# Security
SECRET_KEY=your-secret-key          # JWT secret key (min 32 characters)
ALGORITHM=HS256                     # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30      # Token expiration time in minutes
```

## API Collection Documentation

Maintain a Postman collection or OpenAPI spec with:
- All endpoints documented
- Example requests and responses
- Authentication setup instructions
- Environment variables

## Error Messages

Error messages should be:
- Clear and actionable
- User-friendly (no technical jargon for user-facing errors)
- Logged with details for debugging

```python
# Good
raise ValueError("Email address is already registered")

# Bad
raise ValueError("DB constraint violation: unique_email")
```

## Changelog

Maintain CHANGELOG.md following Keep a Changelog format:

```markdown
# Changelog

## [Unreleased]

## [0.2.0] - 2024-01-20
### Added
- Task CRUD endpoints
- User authentication with JWT

### Changed
- Updated DynamoDB table structure

### Fixed
- Token expiration validation
```

## Documentation Review

Before committing:
- [ ] All public functions have docstrings
- [ ] Complex logic is commented
- [ ] README is up to date
- [ ] API examples are current
- [ ] Type hints are complete
- [ ] Environment variables are documented
- [ ] Architecture docs reflect current state
