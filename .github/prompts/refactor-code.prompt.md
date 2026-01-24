---
agent: 'agent'
model: Claude Sonnet 4
tools: ['edit', 'codebase', 'search']
description: 'Refactor code while maintaining clean architecture principles'
---

# Refactor Code

You are helping refactor code in the servidor backend to improve maintainability while preserving clean architecture.

## Refactoring Goals

- Improve code readability
- Reduce duplication (DRY)
- Enhance testability
- Maintain architecture boundaries
- Improve performance
- Simplify complexity

## Process

### 1. Identify Refactoring Target

Ask the user:
- What code needs refactoring?
- What's the specific problem?
- Any performance concerns?
- Are there tests in place?

### 2. Analyze Current Code

Review the code for:
- Code smells (duplication, long functions, complex logic)
- Architecture violations
- Performance bottlenecks
- Missing abstractions
- Unclear naming

### 3. Common Refactoring Patterns

#### Extract Method

**Before:**
```python
async def create_user(self, dto: CreateUserDTO) -> UserDTO:
    existing = await self.repo.get_by_email(dto.email)
    if existing:
        raise ValueError("Email exists")
    
    if len(dto.password) < 8:
        raise ValueError("Password too short")
    if not re.match(r"[A-Za-z0-9@#$%^&+=]", dto.password):
        raise ValueError("Password invalid")
    
    hashed = self.auth.hash_password(dto.password)
    user = User(email=dto.email, hashed_password=hashed)
    return await self.repo.create(user)
```

**After:**
```python
async def create_user(self, dto: CreateUserDTO) -> UserDTO:
    await self._validate_unique_email(dto.email)
    self._validate_password(dto.password)
    
    hashed = self.auth.hash_password(dto.password)
    user = User(email=dto.email, hashed_password=hashed)
    return await self.repo.create(user)

async def _validate_unique_email(self, email: str):
    if await self.repo.get_by_email(email):
        raise ValueError("Email already exists")

def _validate_password(self, password: str):
    if len(password) < 8:
        raise ValueError("Password too short")
    if not re.match(r"[A-Za-z0-9@#$%^&+=]", password):
        raise ValueError("Password invalid")
```

#### Replace Magic Numbers with Constants

**Before:**
```python
if len(password) < 8:
    raise ValueError("Too short")
```

**After:**
```python
MIN_PASSWORD_LENGTH = 8

if len(password) < MIN_PASSWORD_LENGTH:
    raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
```

#### Extract to Service/Helper

**Before:**
```python
# In use case
def format_task_title(title: str) -> str:
    return title.strip().title()
```

**After:**
```python
# In service
class TaskFormatter:
    @staticmethod
    def format_title(title: str) -> str:
        return title.strip().title()
```

#### Simplify Conditionals

**Before:**
```python
if user.is_active and user.email_verified and not user.is_locked and user.role in ['admin', 'user']:
    return True
return False
```

**After:**
```python
def can_access(self, user: User) -> bool:
    return (
        user.is_active
        and user.email_verified
        and not user.is_locked
        and user.role in self.ALLOWED_ROLES
    )
```

#### Replace Temp with Query

**Before:**
```python
total = base_price * quantity
discount = total * 0.1
final_price = total - discount
return final_price
```

**After:**
```python
def calculate_price(base_price: float, quantity: int) -> float:
    return calculate_total(base_price, quantity) - calculate_discount(base_price, quantity)

def calculate_total(base_price: float, quantity: int) -> float:
    return base_price * quantity

def calculate_discount(base_price: float, quantity: int) -> float:
    return calculate_total(base_price, quantity) * 0.1
```

### 4. Clean Architecture Refactoring

#### Move Business Logic to Domain

**Before (in use case):**
```python
async def complete_task(self, task_id: UUID) -> TaskDTO:
    task = await self.repo.get_by_id(task_id)
    task.completed = True
    task.completed_at = datetime.utcnow()
    return await self.repo.update(task)
```

**After (in entity):**
```python
# Entity
class Task(Entity):
    def mark_as_completed(self):
        self.completed = True
        self.completed_at = datetime.utcnow()

# Use case
async def complete_task(self, task_id: UUID) -> TaskDTO:
    task = await self.repo.get_by_id(task_id)
    task.mark_as_completed()
    return await self.repo.update(task)
```

#### Extract Repository Interface

**Before:**
```python
# Use case directly using implementation
from src.infrastructure.persistence import DynamoDBTaskRepository

class TaskUseCase:
    def __init__(self):
        self.repo = DynamoDBTaskRepository()
```

**After:**
```python
# Domain interface
class TaskRepository(ABC):
    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        pass

# Use case using interface
class TaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo
```

### 5. Performance Refactoring

#### Optimize Queries

**Before:**
```python
# Full table scan
all_users = await repo.get_all()
user_tasks = [u for u in all_users if u.has_tasks()]
```

**After:**
```python
# Indexed query
user_tasks = await repo.get_users_with_tasks()
```

#### Use Batch Operations

**Before:**
```python
for task in tasks:
    await repo.update(task)
```

**After:**
```python
await repo.batch_update(tasks)
```

### 6. Improve Naming

**Before:**
```python
def proc(d):
    return d.get('x')
```

**After:**
```python
def extract_user_id(data: Dict) -> UUID:
    return UUID(data.get('user_id'))
```

### 7. Add Type Safety

**Before:**
```python
async def get_user(id):
    return await repo.get(id)
```

**After:**
```python
async def get_user(user_id: UUID) -> Optional[User]:
    return await repo.get_by_id(user_id)
```

## Refactoring Checklist

Before refactoring:
- [ ] Tests exist and pass
- [ ] Understand current behavior
- [ ] Identify improvement goals
- [ ] Plan the changes

During refactoring:
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Keep commits atomic
- [ ] Maintain architecture boundaries

After refactoring:
- [ ] All tests still pass
- [ ] Code is more readable
- [ ] No functionality changes
- [ ] Performance improved (if goal)
- [ ] Documentation updated

## Safety Rules

**Always:**
- Run tests after each change
- Commit working states frequently
- Keep refactoring separate from features
- Preserve existing behavior

**Never:**
- Refactor without tests
- Mix refactoring with new features
- Break architecture boundaries
- Change public APIs without versioning

## When NOT to Refactor

Avoid refactoring when:
- No tests exist (write tests first)
- Under deadline pressure
- Code works and is rarely changed
- Changes would break public API

## Output Format

Provide:
1. **Analysis**: What needs refactoring and why
2. **Plan**: Step-by-step refactoring approach
3. **Changes**: Actual code changes
4. **Tests**: Verify tests still pass
5. **Summary**: What improved

Ask the user what code they want to refactor!
