---
agent: 'agent'
model: Claude Sonnet 4
tools: ['codebase', 'search', 'runCommands']
description: 'Debug issues and find root causes'
---

# Debug Issue

You are helping debug issues in the servidor backend application.

## Debugging Process

### 1. Gather Information

Ask the user:
- What is the expected behavior?
- What is the actual behavior?
- When did this start happening?
- Can you reproduce it consistently?
- Any error messages or stack traces?
- What data/inputs trigger the issue?

### 2. Reproduce the Issue

Try to reproduce the problem:
- Run the application locally
- Execute the failing request
- Run the test that fails
- Check logs for errors

### 3. Common Issues by Layer

#### Domain Layer Issues

**Problem: Business rule not enforced**
```python
# Check entity methods
class Task:
    def mark_as_completed(self):
        # Is this setting all required fields?
        self.completed = True
        # Missing: self.completed_at = datetime.utcnow()
```

**Problem: Entity state inconsistent**
- Check entity constructors
- Verify business method logic
- Look for missing validations

#### Application Layer Issues

**Problem: Use case not working**
```python
# Check use case logic
async def create_task(self, dto, user_id):
    # Is repository method correct?
    task = Task(...)
    result = await self.repo.create(task)
    # Are we converting back to DTO?
    return self._to_dto(result)
```

Common issues:
- Not handling None returns from repository
- Missing DTO conversions
- Incorrect error handling
- Repository method called wrong

#### Infrastructure Layer Issues

**Problem: DynamoDB not returning data**
```python
# Check DynamoDB operations
response = self.table.query(
    KeyConditionExpression=Key('id').eq(task_id)  # Should be str(task_id)
)
```

Debug steps:
1. Check DynamoDB table exists
2. Verify key schema matches
3. Confirm data types (UUID → str)
4. Check indexes are configured
5. Verify LocalStack is running

**Problem: AWS connectivity**
```bash
# Check LocalStack
docker ps | grep localstack

# Check endpoint URL
echo $AWS_ENDPOINT_URL

# Test connection
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

#### Presentation Layer Issues

**Problem: Authentication not working**
```python
# Check token validation
@router.get("/protected")
async def protected_route(
    current_user: UserDTO = Depends(get_current_active_user)  # Is dependency correct?
):
    pass
```

Debug steps:
1. Check token in request headers
2. Verify token format (Bearer <token>)
3. Check token expiration
4. Verify secret key matches
5. Check user exists in database

**Problem: Request validation failing**
```python
# Check Pydantic schema
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)  # What validation is failing?
    description: Optional[str] = None
```

### 4. Debugging Techniques

#### Add Logging

```python
from src.infrastructure.config import logger

async def create_task(self, dto, user_id):
    logger.debug(f"Creating task for user {user_id}")
    logger.debug(f"Task data: {dto}")
    
    try:
        task = Task(...)
        logger.debug(f"Created task entity: {task.id}")
        
        result = await self.repo.create(task)
        logger.debug(f"Saved task to database: {result}")
        
        return self._to_dto(result)
    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        raise
```

#### Check Database State

```python
# In Python console
from src.infrastructure.persistence import DynamoDBTaskRepository
repo = DynamoDBTaskRepository()

# Check if data exists
tasks = await repo.get_by_user_id(user_id)
print(f"Found {len(tasks)} tasks")

# Check specific item
task = await repo.get_by_id(task_id)
print(f"Task: {task}")
```

#### Test Individual Components

```python
# Test entity
task = Task(title="Test", user_id=user_id)
task.mark_as_completed()
assert task.completed is True

# Test repository
repo = DynamoDBTaskRepository()
saved = await repo.create(task)
retrieved = await repo.get_by_id(saved.id)
assert retrieved is not None

# Test use case
use_case = TaskUseCase(repo)
dto = CreateTaskDTO(title="Test")
result = await use_case.create_task(dto, user_id)
assert result.title == "Test"
```

#### Use Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use IDE debugger
# Set breakpoint in VS Code / PyCharm
```

### 5. Common Error Patterns

#### TypeError: object is not subscriptable

```python
# Problem: Treating None as dict
user = await repo.get_by_id(user_id)  # Returns None
email = user['email']  # ERROR!

# Solution: Check for None
user = await repo.get_by_id(user_id)
if not user:
    raise ValueError("User not found")
email = user.email
```

#### AttributeError: NoneType has no attribute

```python
# Problem: Not handling None
task = await repo.get_by_id(task_id)  # Returns None
task.mark_as_completed()  # ERROR!

# Solution: Check for None
task = await repo.get_by_id(task_id)
if not task:
    raise ValueError("Task not found")
task.mark_as_completed()
```

#### KeyError in DynamoDB

```python
# Problem: Key doesn't match schema
response = table.get_item(Key={'task_id': str(task_id)})
# Table uses 'id' not 'task_id'!

# Solution: Use correct key name
response = table.get_item(Key={'id': str(task_id)})
```

#### ValidationError from Pydantic

```python
# Problem: Data type mismatch
TaskCreate(title=123)  # title expects str

# Solution: Convert types
TaskCreate(title=str(123))

# Or check API request
curl -X POST /api/v1/tasks -d '{"title": 123}'  # Should be string
```

#### 401 Unauthorized

Common causes:
1. Missing Authorization header
2. Token expired
3. Wrong token format (missing "Bearer ")
4. Secret key mismatch
5. User not found/inactive

Debug:
```python
# Check token
print(f"Token: {token}")
payload = jwt.decode(token, secret_key, algorithms=['HS256'])
print(f"Payload: {payload}")

# Check user
user_id = payload.get('sub')
user = await repo.get_by_id(user_id)
print(f"User: {user}")
print(f"Active: {user.is_active}")
```

### 6. Performance Issues

#### Slow Queries

```python
# Add timing
import time

start = time.time()
tasks = await repo.get_by_user_id(user_id)
duration = time.time() - start

if duration > 1.0:
    logger.warning(f"Slow query: {duration:.2f}s")
```

Check:
- Is query using index?
- Is it a table scan?
- Too much data returned?

#### Memory Issues

```python
# Check memory usage
import tracemalloc

tracemalloc.start()
# Run code
await process_large_dataset()
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.1f}MB, Peak: {peak / 1024 / 1024:.1f}MB")
tracemalloc.stop()
```

### 7. Testing the Fix

After fixing:
1. Verify issue is resolved
2. Add regression test
3. Check related functionality
4. Review logs for other errors
5. Test edge cases

```python
# Add test for the bug
@pytest.mark.asyncio
async def test_task_completion_bug_fix():
    """Regression test for task completion not setting timestamp."""
    task = Task(title="Test", user_id=user_id)
    task.mark_as_completed()
    
    assert task.completed is True
    assert task.completed_at is not None  # This was the bug!
```

## Debugging Checklist

- [ ] Understand expected vs actual behavior
- [ ] Reproduce the issue
- [ ] Check error messages and logs
- [ ] Verify environment (LocalStack running, etc.)
- [ ] Test individual components
- [ ] Add logging at key points
- [ ] Check data types and conversions
- [ ] Verify architecture boundaries
- [ ] Test the fix
- [ ] Add regression test

## Output Format

Provide:
1. **Root Cause**: What caused the issue
2. **Fix**: Code changes to resolve it
3. **Verification**: How to verify it's fixed
4. **Prevention**: How to prevent in future
5. **Test**: Regression test to add

Ask the user to describe the issue they're experiencing!
