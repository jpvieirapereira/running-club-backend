<!-- Based on: https://github.com/github/awesome-copilot/blob/main/instructions/python.instructions.md -->
---
description: 'Python coding conventions and guidelines for servidor backend'
applyTo: '**/*.py'
---

# Python Coding Conventions

## Python Instructions

- Write clear and concise comments for each function.
- Ensure functions have descriptive names and include type hints.
- Provide docstrings following PEP 257 conventions.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`, `Optional[T]`).
- Break down complex functions into smaller, more manageable functions.

## Clean Architecture Specific

- **Domain entities** must not import from FastAPI, boto3, or any external framework
- **Use cases** should only import from domain layer and DTOs
- **Repository implementations** go in `infrastructure/persistence/`
- **Repository interfaces** go in `domain/repositories/`
- Use dependency injection for all services

## General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Code Style and Formatting

- Follow the **PEP 8** style guide for Python.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Ensure lines do not exceed 88 characters (Black formatter standard).
- Place function and class docstrings immediately after the `def` or `class` keyword.
- Use blank lines to separate functions, classes, and code blocks where appropriate.
- Use f-strings for string formatting.
- Prefer `pathlib` over `os.path` for file operations.

## Type Hints

- Use type hints for all function parameters and return values
- Import from `typing` for generic types
- Use `Optional[T]` for nullable types
- For async functions, return type should reflect awaitable (e.g., `-> User:`)

Example:
```python
from typing import Optional, List
from uuid import UUID

async def get_user(user_id: UUID) -> Optional[User]:
    """Get user by ID."""
    pass
```

## Async/Await

- Use `async def` for all repository methods
- Use `await` when calling async functions
- Repository implementations can be sync internally (boto3), but interface should be async
- FastAPI route handlers should be async when calling use cases

## Edge Cases and Testing

- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.

## FastAPI Specific

- Use Pydantic models for request/response validation
- Use dependency injection via `Depends()`
- Keep route handlers thin - delegate to use cases
- Use proper HTTP status codes
- Add OpenAPI documentation with descriptions

## AWS & DynamoDB

- Use `boto3.resource` for DynamoDB operations
- Handle AWS exceptions appropriately
- Use LocalStack endpoint for local development
- Always convert UUIDs to strings for DynamoDB storage

## Example of Proper Documentation

```python
from typing import Optional
from uuid import UUID

async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
    """
    Get user by ID from DynamoDB.
    
    Args:
        user_id: The unique identifier of the user
    
    Returns:
        User entity if found, None otherwise
    
    Raises:
        ValueError: If user_id is invalid
    """
    response = self.table.get_item(Key={'id': str(user_id)})
    item = response.get('Item')
    return self._from_item(item) if item else None
```
