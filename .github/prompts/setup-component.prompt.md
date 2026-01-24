---
agent: 'agent'
model: Claude Sonnet 4
tools: ['edit', 'codebase', 'search']
description: 'Create a new component following clean architecture patterns'
---

# Create New Component

You are helping create a new component in the servidor backend following clean architecture principles.

## Process

### 1. Gather Requirements
Ask the user for:
- Component name (e.g., "Project", "Comment", "Notification")
- Component purpose and main responsibilities
- Key attributes/fields
- Relationships to existing entities

### 2. Create Domain Layer Files

**Entity** (`src/domain/entities/{component}.py`):
- Inherit from `Entity` base class
- Define attributes with type hints
- Add business methods (e.g., `activate()`, `complete()`)
- No external dependencies

**Repository Interface** (`src/domain/repositories/{component}_repository.py`):
- Inherit from `ABC`
- Define async abstract methods
- Include CRUD operations
- Use domain types only

### 3. Create Application Layer Files

**DTOs** (`src/application/dtos/{component}_dto.py`):
- Create DTOs for different operations:
  - `{Component}DTO` - full representation
  - `Create{Component}DTO` - for creation
  - `Update{Component}DTO` - for updates

**Use Case** (`src/application/use_cases/{component}_use_case.py`):
- Create `{Component}UseCase` class
- Inject repository via constructor
- Implement business workflows
- Use DTOs for input/output
- Handle validation and errors

### 4. Create Infrastructure Layer

**Repository Implementation** (`src/infrastructure/persistence/dynamodb_{component}_repository.py`):
- Implement the repository interface
- Handle DynamoDB operations
- Convert between entities and items
- Use proper error handling

### 5. Create Presentation Layer

**Schema** (`src/presentation/schemas/{component}_schema.py`):
- Create Pydantic models for API:
  - `{Component}Create`
  - `{Component}Update`
  - `{Component}Response`
- Add validation and examples

**API Routes** (`src/presentation/api/v1/{component}s.py`):
- Create router with endpoints:
  - `POST /{components}` - create
  - `GET /{components}` - list
  - `GET /{components}/{id}` - get by ID
  - `PUT /{components}/{id}` - update
  - `DELETE /{components}/{id}` - delete
- Use authentication dependencies
- Add OpenAPI documentation

### 6. Wire Dependencies

**Update Container** (`src/infrastructure/container.py`):
- Add repository provider
- Add use case provider with dependencies

**Update Router** (`src/presentation/api/v1/__init__.py`):
- Include new router in api_router

### 7. Create AWS Resources

**Update Initializer** (`src/infrastructure/aws/initializer.py`):
- Add DynamoDB table creation
- Define key schema and indexes
- Add to .env.example with table name

### 8. Add Tests

Create test files:
- `tests/domain/test_{component}.py` - entity tests
- `tests/application/test_{component}_use_case.py` - use case tests
- `tests/api/test_{component}_api.py` - API tests

## Example Flow

For a "Project" component:

1. **Domain**: `Project` entity with `name`, `description`, `owner_id`
2. **Application**: `ProjectUseCase` with CRUD operations
3. **Infrastructure**: `DynamoDBProjectRepository`
4. **Presentation**: Project API endpoints
5. **Container**: Wire all dependencies
6. **AWS**: Create `projects` DynamoDB table
7. **Tests**: Comprehensive test coverage

## Architecture Rules

- Domain layer has no external dependencies
- Use cases only import from domain
- Infrastructure implements interfaces
- Presentation uses dependency injection
- All layers follow single responsibility

## Validation

Before completing, verify:
- [ ] All layers created
- [ ] Dependencies point inward
- [ ] Tests added
- [ ] Documentation updated
- [ ] Container wired
- [ ] AWS resources configured
- [ ] API endpoints work
- [ ] Authentication applied

Start by asking what component the user wants to create!
