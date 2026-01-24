---
description: 'Code review standards and GitHub review guidelines'
applyTo: '**/*'
---

# Code Review Standards

## Code Review Goals

- Maintain code quality and consistency
- Share knowledge across the team
- Catch bugs and security issues early
- Ensure adherence to architecture principles
- Improve code readability and maintainability

## What to Review

### Architecture & Design
- [ ] Follows clean architecture layer boundaries
- [ ] Dependencies point in the correct direction
- [ ] No business logic in presentation layer
- [ ] Repository interfaces used (not implementations)
- [ ] Proper use of dependency injection

### Code Quality
- [ ] Code is readable and self-explanatory
- [ ] Functions have single responsibility
- [ ] DRY principle followed (no duplication)
- [ ] Appropriate error handling
- [ ] Type hints present and accurate

### Testing
- [ ] Tests cover new functionality
- [ ] Edge cases are tested
- [ ] Tests are meaningful (not just coverage)
- [ ] Integration tests for critical paths
- [ ] Mocks used appropriately

### Security
- [ ] No secrets in code
- [ ] Input validation present
- [ ] Authentication/authorization checked
- [ ] SQL/NoSQL injection prevented
- [ ] Sensitive data not logged

### Performance
- [ ] No obvious performance issues
- [ ] Async/await used correctly
- [ ] Database queries optimized
- [ ] No unnecessary loops or operations
- [ ] Appropriate data structures used

### Documentation
- [ ] Public functions have docstrings
- [ ] Complex logic is commented
- [ ] README updated if needed
- [ ] API documentation current
- [ ] Type hints complete

## Clean Architecture Review Checklist

### Domain Layer
- [ ] No imports from outer layers
- [ ] No framework dependencies
- [ ] Pure business logic only
- [ ] Entities properly modeled
- [ ] Repository interfaces defined

### Application Layer
- [ ] Only imports from domain
- [ ] Use cases orchestrate properly
- [ ] DTOs used for data transfer
- [ ] No direct framework usage
- [ ] Business workflows clear

### Infrastructure Layer
- [ ] Implements domain interfaces
- [ ] Handles external services
- [ ] Configuration properly managed
- [ ] AWS clients configured correctly
- [ ] Repository implementations correct

### Presentation Layer
- [ ] Thin controllers (delegate to use cases)
- [ ] Request/response validation
- [ ] Proper HTTP status codes
- [ ] Authentication dependencies used
- [ ] No business logic

## Review Process

### 1. Self-Review First

Before requesting review:
- Review your own changes
- Run tests locally
- Check linting and formatting
- Verify documentation is updated
- Test the changes manually

### 2. Creating Pull Requests

**Good PR Title:**
```
feat: add task completion endpoint
fix: correct user authentication validation
refactor: improve DynamoDB query performance
```

**PR Description Template:**
```markdown
## Description
Brief description of changes and why they're needed.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring
- [ ] Documentation update

## Changes Made
- Added task completion endpoint
- Updated task entity with complete() method
- Added tests for new functionality

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes
```

### 3. Reviewing PRs

**Review Approach:**
1. Read the PR description
2. Understand the problem being solved
3. Review architecture/design first
4. Then review implementation details
5. Check tests and documentation
6. Test locally if significant changes

**Comment Types:**

**Blocking Issues (Request Changes):**
```
❌ Security issue: Password not hashed before storage
❌ Architecture violation: Use case importing from infrastructure
❌ Breaking change: API contract changed without versioning
```

**Suggestions (Approve with comments):**
```
💡 Consider: Could use a set here for O(1) lookup
💡 Suggestion: This could be extracted to a helper function
💡 Naming: `get_user_tasks` might be clearer than `fetch_tasks`
```

**Questions (For understanding):**
```
❓ Question: Why is this check needed here?
❓ Clarification: Is this handling the edge case of empty list?
```

**Praise (Encourage good work):**
```
✅ Nice: Great test coverage on this feature
✅ Good: Clean separation of concerns here
✅ Excellent: Well-documented function
```

### 4. Responding to Reviews

**Good Responses:**
```
✅ Fixed: Password now hashed with bcrypt
✅ Refactored: Extracted to `calculate_total()` helper
✅ Clarified: Added comment explaining the edge case
✅ Discussed: Let's talk about this approach in standup
```

**Avoid:**
```
❌ "It works fine"
❌ "This is how I always do it"
❌ "Not important"
❌ No response at all
```

## Review Guidelines by Component

### Entity Changes
- Business rules properly encapsulated
- No external dependencies
- Validation logic in entity
- Immutability where appropriate

### Repository Changes
- Interface matches implementation
- Async methods properly implemented
- Error handling appropriate
- Type conversions correct (UUID ↔ str)

### Use Case Changes
- Single responsibility maintained
- Dependencies injected
- DTOs used correctly
- Business logic clear

### API Endpoint Changes
- Request/response schemas defined
- Authentication required if needed
- HTTP status codes appropriate
- Error handling present
- OpenAPI documentation updated

## Common Issues to Catch

### Architecture Violations
```python
# ❌ Bad: Domain importing from infrastructure
from src.infrastructure.persistence import DynamoDBUserRepository

# ✅ Good: Domain only uses interface
from src.domain.repositories import UserRepository
```

### Missing Error Handling
```python
# ❌ Bad: No error handling
user = await repo.get_by_id(user_id)
return user.email

# ✅ Good: Handle not found case
user = await repo.get_by_id(user_id)
if not user:
    raise ValueError("User not found")
return user.email
```

### Security Issues
```python
# ❌ Bad: No password hashing
user = User(email=email, password=password)

# ✅ Good: Hash password
hashed = auth_service.hash_password(password)
user = User(email=email, hashed_password=hashed)
```

### Missing Type Hints
```python
# ❌ Bad: No type hints
async def get_user(id):
    return await repo.get(id)

# ✅ Good: Clear types
async def get_user(user_id: UUID) -> Optional[User]:
    return await repo.get_by_id(user_id)
```

## Review Response Time

- **Critical bugs**: Review within 2 hours
- **Regular PRs**: Review within 24 hours
- **Large PRs**: May take longer, split if possible

## Large PR Guidelines

If PR is large (>500 lines):
- Consider splitting into smaller PRs
- Provide detailed description
- Highlight critical changes
- Schedule synchronous review if needed

## Merge Criteria

PR can be merged when:
- [ ] At least one approval received
- [ ] All comments addressed
- [ ] CI/CD pipeline passes
- [ ] No merge conflicts
- [ ] All reviewers' concerns resolved

## Post-Merge

After merging:
- Delete the feature branch
- Monitor for issues in staging
- Update issue tracker
- Celebrate the contribution! 🎉

## Review Etiquette

**Do:**
- Be respectful and constructive
- Focus on the code, not the person
- Explain the "why" behind suggestions
- Acknowledge good work
- Ask questions to understand

**Don't:**
- Use harsh or negative language
- Nitpick on style (use linters instead)
- Block PRs for personal preferences
- Rush through reviews
- Ignore context or constraints
