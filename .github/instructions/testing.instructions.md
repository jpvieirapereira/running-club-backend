---
description: 'Testing standards and practices for servidor backend'
applyTo: '**/test_*.py,**/*_test.py'
---

# Testing Guidelines

## Testing Strategy

Follow the testing pyramid approach:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **API Tests**: Test complete request/response cycles

## Test Organization

### Directory Structure
- All tests go in `tests/` directory
- Mirror the source structure: `tests/domain/`, `tests/application/`, etc.
- Name test files with `test_` prefix: `test_user_repository.py`

### Test Naming
- Test functions: `test_<functionality>_<scenario>_<expected_result>`
- Examples:
  - `test_create_user_with_valid_data_returns_user`
  - `test_login_with_invalid_password_raises_error`
  - `test_get_task_not_found_returns_none`

## Testing Clean Architecture Layers

### Domain Layer (Entities)
- Test business rules and entity behavior
- No external dependencies required
- Fast, pure unit tests

Example:
```python
def test_task_mark_as_completed_sets_completed_flag():
    task = Task(title="Test", user_id=uuid4())
    task.mark_as_completed()
    assert task.completed is True
```

### Application Layer (Use Cases)
- Mock repository interfaces
- Test business workflows
- Focus on orchestration logic

Example:
```python
@pytest.mark.asyncio
async def test_create_task_calls_repository():
    mock_repo = Mock(spec=TaskRepository)
    use_case = TaskUseCase(mock_repo)
    
    dto = CreateTaskDTO(title="Test")
    await use_case.create_task(dto, user_id=uuid4())
    
    mock_repo.create.assert_called_once()
```

### Infrastructure Layer (Repositories)
- Use LocalStack or moto for AWS services
- Test actual DynamoDB operations
- Verify data persistence and retrieval

### Presentation Layer (API)
- Use `httpx.AsyncClient` for API testing
- Test authentication flows
- Verify response schemas

## Test Requirements

### What to Test
- All public methods and functions
- Business rule validations
- Error handling and edge cases
- Authentication and authorization
- Data validation and transformation

### What NOT to Test
- Framework code (FastAPI, boto3)
- External libraries
- Configuration loading (unless custom logic)
- Simple getters/setters without logic

## Pytest Configuration

Use these fixtures and markers:
- `@pytest.mark.asyncio` for async tests
- `@pytest.fixture` for reusable test data
- `@pytest.mark.integration` for integration tests
- `@pytest.mark.unit` for unit tests

## Mocking Guidelines

### When to Mock
- External services (AWS, databases)
- Repository interfaces in use case tests
- Authentication in API tests

### When NOT to Mock
- Domain entities (test the real thing)
- Simple data structures
- Internal application logic

### Mocking Tools
- Use `unittest.mock.Mock` for simple mocks
- Use `pytest.fixture` for complex test data
- Use `moto` for AWS service mocking
- Use LocalStack for integration tests

## Assertions

- Use clear, descriptive assertions
- Test one thing per test function
- Use pytest's rich assertion introspection
- Assert on meaningful values, not implementation details

Good assertions:
```python
assert user.email == "test@example.com"
assert len(tasks) == 3
assert response.status_code == 201
assert "Task not found" in str(exception)
```

Avoid:
```python
assert user  # Too vague
assert True  # Meaningless
```

## Test Data

- Use factories or fixtures for test data
- Keep test data minimal and focused
- Use realistic but not production data
- Avoid hardcoded IDs (use uuid4())

## Coverage Goals

- Aim for >80% code coverage
- Focus on critical business logic paths
- Don't chase 100% coverage for trivial code
- Use `pytest --cov` to measure coverage

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=src tests/

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Test Performance

- Unit tests should run in milliseconds
- Integration tests can take seconds
- Use `pytest-timeout` to catch slow tests
- Mock expensive operations in unit tests
