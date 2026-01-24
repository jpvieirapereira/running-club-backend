---
agent: 'agent'
model: Claude Sonnet 4
tools: ['edit', 'codebase', 'create']
description: 'Generate comprehensive tests for existing code'
---

# Write Tests

You are helping write comprehensive tests for the servidor backend application.

## Test Strategy

### Test Pyramid
1. **Unit Tests** (majority) - Fast, isolated, no external dependencies
2. **Integration Tests** - Test component interactions
3. **API Tests** - End-to-end request/response cycles

## Process

### 1. Identify What to Test

Ask the user:
- What component/feature needs tests?
- What's the current test coverage?
- Any specific scenarios to cover?

### 2. Analyze the Code

Using the codebase tool:
- Find the target component
- Identify public methods
- List dependencies
- Note edge cases

### 3. Write Unit Tests

**For Entities** (`tests/domain/test_{entity}.py`):
```python
import pytest
from uuid import uuid4
from src.domain.entities.{entity} import {Entity}

def test_{entity}_creation():
    entity = {Entity}(name="Test", ...)
    assert entity.name == "Test"
    assert entity.id is not None

def test_{entity}_business_method():
    entity = {Entity}(...)
    entity.some_method()
    assert entity.state == expected_state
```

**For Use Cases** (`tests/application/test_{use_case}.py`):
```python
import pytest
from unittest.mock import Mock, AsyncMock
from src.application.use_cases.{use_case} import {UseCase}
from src.domain.repositories.{repository} import {Repository}

@pytest.mark.asyncio
async def test_{usecase}_success():
    # Arrange
    mock_repo = Mock(spec={Repository})
    mock_repo.create = AsyncMock(return_value=expected)
    use_case = {UseCase}(mock_repo)
    
    # Act
    result = await use_case.method(dto)
    
    # Assert
    assert result == expected
    mock_repo.create.assert_called_once()
```

### 4. Write Integration Tests

**For Repositories** (`tests/infrastructure/test_{repository}.py`):
```python
import pytest
from src.infrastructure.persistence.dynamodb_{repository} import DynamoDB{Repository}

@pytest.mark.integration
@pytest.mark.asyncio
async def test_repository_create():
    repo = DynamoDB{Repository}()
    entity = {Entity}(...)
    
    result = await repo.create(entity)
    
    assert result.id is not None
    # Verify in database
    found = await repo.get_by_id(result.id)
    assert found is not None
```

### 5. Write API Tests

**For Endpoints** (`tests/api/test_{endpoint}_api.py`):
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_{resource}(client: AsyncClient, auth_token: str):
    response = await client.post(
        "/api/v1/{resources}",
        json={"name": "Test", ...},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
    assert "id" in data
```

### 6. Test Edge Cases

Cover these scenarios:
- **Empty inputs**: What happens with empty strings, lists?
- **Invalid data**: What about wrong types, out-of-range values?
- **Not found**: What if resource doesn't exist?
- **Unauthorized**: What if user doesn't have permission?
- **Duplicates**: What if resource already exists?
- **Concurrency**: What about race conditions?

### 7. Test Error Handling

```python
@pytest.mark.asyncio
async def test_{method}_raises_error_when_invalid():
    use_case = {UseCase}(mock_repo)
    
    with pytest.raises(ValueError, match="Invalid input"):
        await use_case.method(invalid_dto)
```

## Test Quality Guidelines

### Good Tests
- **Descriptive names**: `test_create_user_with_duplicate_email_raises_error`
- **AAA pattern**: Arrange, Act, Assert
- **Single assertion focus**: Test one thing per test
- **Independent**: Tests don't depend on each other
- **Fast**: Unit tests run in milliseconds

### What NOT to Test
- Framework code (FastAPI, boto3)
- External libraries
- Simple property getters
- Configuration values

## Fixtures

Create reusable fixtures in `tests/conftest.py`:

```python
import pytest
from httpx import AsyncClient
from src.presentation.api.app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_token(client):
    # Register and login
    response = await client.post("/api/v1/auth/register", json={...})
    response = await client.post("/api/v1/auth/login", data={...})
    return response.json()["access_token"]
```

## Mocking Guidelines

### When to Mock
- External services (AWS, databases in unit tests)
- Repository interfaces in use case tests
- Time/randomness for deterministic tests

### When NOT to Mock
- Domain entities (test real ones)
- Simple data structures
- Your own business logic

### Mock Tools
- `unittest.mock.Mock` - synchronous mocks
- `unittest.mock.AsyncMock` - async mocks
- `pytest.fixture` - test data and setup
- `moto` - AWS service mocking

## Coverage

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html tests/
```

Aim for:
- **>80% overall coverage**
- **>90% for business logic**
- **>70% for infrastructure**

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── domain/
│   ├── test_user.py
│   └── test_task.py
├── application/
│   ├── test_auth_use_case.py
│   └── test_task_use_case.py
├── infrastructure/
│   ├── test_user_repository.py
│   └── test_task_repository.py
└── api/
    ├── test_auth_api.py
    └── test_tasks_api.py
```

## Validation

Before completing, ensure:
- [ ] Tests follow naming conventions
- [ ] AAA pattern used consistently
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Mocks used appropriately
- [ ] Tests are independent
- [ ] Coverage is adequate
- [ ] All tests pass

Ask the user what they want to test, then generate comprehensive tests!
