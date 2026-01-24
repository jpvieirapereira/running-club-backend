# Running Training Platform Backend

A Python backend for a running training platform following Clean Architecture principles with FastAPI. Supports multiple user types (Admins, Coaches, Customers), training plan management, and Strava integration. Deployable as both ASGI and AWS Lambda.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📑 Table of Contents

- [What is Running App?](#-what-is-running)
- [Features](#-features)
- [Architecture](#️-architecture)
- [Quick Start](#-quick-start)
- [Development](#-development)
- [API Documentation](#-api-documentation)
- [CLI Commands](#️-cli-commands)
- [Deployment](#-deployment)
- [Configuration](#️-configuration)
- [Testing](#-testing)
- [Clean Architecture Benefits](#️-clean-architecture-benefits)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [Tech Stack](#-tech-stack)
- [Troubleshooting](#-troubleshooting)

## 🏃 What is Running App?

Running App is a comprehensive backend API for managing running training programs. It enables:
- **Coaches** to create and manage training plans for their athletes
- **Customers** (athletes) to view their training plans and sync activities from Strava
- **Admins** to manage the platform and users
- **Automatic Activity Tracking** via Strava webhooks

## 📋 Features

### Core Features
- ✅ **Multi-User System**: Admin, Coach, and Customer roles with distinct permissions
- ✅ **Training Plan Management**: Full CRUD for training plans with weekly schedules
- ✅ **Strava Integration**: OAuth2 connection, activity sync, and webhook support
- ✅ **JWT Authentication**: Secure OAuth2 password flow with role-based access
- ✅ **Clean Architecture**: Clear separation of concerns with dependency inversion
- ✅ **Multiple Entrypoints**: ASGI, AWS Lambda, and CLI support

### Technical Features
- ✅ **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- ✅ **DynamoDB**: Scalable NoSQL database for users, training plans, and activities
- ✅ **S3**: File storage for training plan attachments
- ✅ **LocalStack**: Local AWS service emulation for development
- ✅ **Dependency Injection**: Using `dependency-injector` for IoC
- ✅ **Type Safety**: Full type hints with Pydantic validation
- ✅ **Docker Support**: Complete Docker Compose setup for local development

## 🏗️ Architecture

```
servidor/
├── src/
│   ├── domain/              # Enterprise Business Rules
│   │   ├── entities/        # User, Coach, Customer, TrainingPlan, etc.
│   │   └── repositories/    # Repository interfaces
│   ├── application/         # Application Business Rules
│   │   ├── use_cases/       # Business workflows
│   │   └── dtos/            # Data Transfer Objects
│   ├── infrastructure/      # Frameworks & Drivers
│   │   ├── persistence/     # DynamoDB repository implementations
│   │   ├── aws/             # AWS service clients
│   │   ├── auth/            # JWT & password hashing
│   │   ├── config/          # Configuration management
│   │   └── container.py     # Dependency Injection container
│   └── presentation/        # Interface Adapters
│       ├── api/v1/          # API routes (auth, training_plans, strava, etc.)
│       ├── schemas/         # Pydantic request/response models
│       ├── middleware/      # Error handling, logging
│       └── dependencies.py  # FastAPI dependencies
├── entrypoints/
│   ├── asgi.py             # ASGI entrypoint (Uvicorn)
│   ├── lambda_handler.py   # AWS Lambda handler (Mangum)
│   └── cli.py              # CLI for admin tasks
└── tests/                  # Test suite (pytest)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.



## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **UV** (recommended) or pip

### 1. Install UV (Fast Python Package Manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
git clone <repository-url>
cd servidor
make setup  # Creates .env from template and installs dependencies
```

Or manually:
```bash
cp .env.example .env
uv pip install -r pyproject.toml
```

### 3. Configure Environment

Edit `.env` and set your Strava API credentials (get them from https://www.strava.com/settings/api):

```bash
STRAVA_CLIENT_ID=your_actual_client_id
STRAVA_CLIENT_SECRET=your_actual_client_secret
STRAVA_CALLBACK_URL=http://localhost:8000/api/v1/strava/callback
```

### 4. Start Services

```bash
# Option 1: Full stack with Docker (Recommended)
make docker-up

# Option 2: Local development (requires LocalStack)
make localstack  # Terminal 1
make run         # Terminal 2
```

The application will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **LocalStack**: http://localhost:4566

### 5. Create Admin User

```bash
python -m entrypoints.cli create-admin \
    --email admin@example.com \
    --password Admin123! \
    --name "System Admin" \
    --phone "11999999999" \
    --dob "1985-01-01"
```

See [QUICKSTART.md](QUICKSTART.md) for step-by-step API testing.

## 💻 Development

### Available Commands

```bash
make help          # Show all available commands
make setup         # Initial setup (creates .env, installs deps)
make install       # Install dependencies with UV
make dev           # Install with dev dependencies
make run           # Run locally (requires LocalStack running)
make test          # Run test suite
make docker-up     # Start with Docker Compose
make docker-down   # Stop Docker services
make docker-logs   # Follow Docker logs
make localstack    # Start only LocalStack
make clean         # Clean cache and build files
```

### Local Development (Without Docker)

1. Start LocalStack:
```bash
make localstack
```

2. In another terminal, run the API:
```bash
make run
# Or directly:
uvicorn entrypoints.asgi:app --reload
```

### Project Structure

#### Domain Layer (Pure Business Logic)
- **Entities**: `User`, `Admin`, `Coach`, `Customer`, `TrainingPlan`, `TrainingDay`, `StravaActivity`, `StravaConnection`
- **Enums**: `UserType`, `TrainingType`, `IntensityLevel`, `WeekDay`
- **Repository Interfaces**: Define data access contracts
- **No external dependencies** - framework-agnostic

#### Application Layer (Use Cases)
- **AuthenticationUseCase**: User registration, login, profile management
- **TrainingPlanUseCase**: CRUD for training plans and days
- **StravaUseCase**: OAuth flow, activity sync, connection management
- **DTOs**: Clean data transfer between layers

#### Infrastructure Layer (External Services)
- **DynamoDB Repositories**: Implement domain repository interfaces
- **AWS Clients**: S3, DynamoDB resource factories
- **Auth Service**: JWT token generation/validation, password hashing (bcrypt)
- **Configuration**: Environment-based settings with Pydantic
- **Container**: Dependency injection wiring

#### Presentation Layer (HTTP API)
- **Routes**: `/api/v1/auth`, `/api/v1/training-plans`, `/api/v1/strava`, `/api/v1/public`, `/api/v1/webhooks`
- **Schemas**: Pydantic models for request/response validation
- **Dependencies**: `get_current_user`, `get_current_coach`, `get_current_customer`
- **Middleware**: Error handling, CORS, request logging

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs (Try out endpoints directly)
- **ReDoc**: http://localhost:8000/redoc (Clean documentation view)

### API Endpoints

#### 🔐 Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register/coach` | Register new coach | ❌ |
| POST | `/register/customer` | Register new customer | ❌ |
| POST | `/login` | Login (form-data) | ❌ |
| POST | `/login-json` | Login (JSON) | ❌ |
| GET | `/me` | Get current user profile | ✅ |
| PUT | `/me` | Update profile | ✅ |
| GET | `/coaches` | List all coaches | ✅ Customer |
| GET | `/coaches/{id}/customers` | Get coach's customers | ✅ Coach |
| PUT | `/customers/assign-coach` | Assign coach to customer | ✅ Customer |

#### 🏃 Training Plans (`/api/v1/training-plans`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create training plan | ✅ Coach |
| GET | `/{plan_id}` | Get training plan | ✅ |
| GET | `/` | List training plans | ✅ |
| PUT | `/{plan_id}` | Update training plan | ✅ Coach |
| DELETE | `/{plan_id}` | Delete training plan | ✅ Coach |
| POST | `/{plan_id}/days` | Add training day | ✅ Coach |

#### 🔗 Strava Integration (`/api/v1/strava`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/connect` | Get Strava authorization URL | ✅ |
| GET | `/callback` | OAuth callback (handled by Strava) | ❌ |
| DELETE | `/disconnect` | Disconnect Strava | ✅ |
| GET | `/status` | Check connection status | ✅ |
| POST | `/sync` | Manually sync activities | ✅ |
| GET | `/activities` | List synced activities | ✅ |
| GET | `/activities/{id}` | Get activity details | ✅ |

#### 📢 Webhooks (`/api/v1/webhooks`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/strava` | Verify webhook subscription | ❌ |
| POST | `/strava` | Receive activity updates | ❌ |

#### 🌐 Public (`/api/v1/public`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/enums` | Get all enum values | ❌ |

### API Usage Examples

#### 1. Register as Coach

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/coach \
  -H "Content-Type: application/json" \
  -d '{
    "email": "coach@example.com",
    "password": "SecurePass123!",
    "full_name": "John Coach",
    "phone": "11987654321",
    "date_of_birth": "1985-05-15",
    "specialty": "Marathon Training",
    "bio": "Experienced marathon coach"
  }'
```

#### 2. Register as Customer

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/customer \
  -H "Content-Type: application/json" \
  -d '{
    "email": "athlete@example.com",
    "password": "SecurePass123!",
    "full_name": "Jane Athlete",
    "phone": "11987654321",
    "date_of_birth": "1990-03-20"
  }'
```

#### 3. Login (Get Token)

```bash
# Form-data format (OAuth2 standard)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=coach@example.com&password=SecurePass123!"

# JSON format (alternative)
curl -X POST http://localhost:8000/api/v1/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{
    "email": "coach@example.com",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 4. Create Training Plan (Coach Only)

```bash
TOKEN="your_coach_token_here"

curl -X POST http://localhost:8000/api/v1/training-plans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "customer_id": "customer-uuid-here",
    "start_date": "2024-03-01",
    "end_date": "2024-05-31",
    "goal": "Prepare for first 10K race",
    "notes": "Focus on gradual mileage increase"
  }'
```

#### 5. Add Training Day to Plan

```bash
curl -X POST http://localhost:8000/api/v1/training-plans/{plan_id}/days \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "week_day": "MONDAY",
    "training_type": "EASY_RUN",
    "intensity": "LOW",
    "duration_minutes": 45,
    "distance_km": 7.5,
    "description": "Easy recovery run",
    "notes": "Keep heart rate in Zone 2"
  }'
```

#### 6. Connect Strava

```bash
# Step 1: Get authorization URL
curl -X GET http://localhost:8000/api/v1/strava/connect \
  -H "Authorization: Bearer $TOKEN"

# Returns: {"authorization_url": "https://www.strava.com/oauth/authorize?..."}
# Open this URL in browser to authorize

# Step 2: Check connection status
curl -X GET http://localhost:8000/api/v1/strava/status \
  -H "Authorization: Bearer $TOKEN"
```

#### 7. Sync Strava Activities

```bash
curl -X POST http://localhost:8000/api/v1/strava/sync \
  -H "Authorization: Bearer $TOKEN"
```

#### 8. Get Customer's Training Plans

```bash
# As customer
curl -X GET http://localhost:8000/api/v1/training-plans \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"

# As coach (see all plans you created)
curl -X GET http://localhost:8000/api/v1/training-plans \
  -H "Authorization: Bearer $COACH_TOKEN"
```

#### 9. Customer Selects a Coach

```bash
curl -X PUT http://localhost:8000/api/v1/auth/customers/assign-coach \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -d '{
    "coach_id": "coach-uuid-here"
  }'
```

#### 10. List Available Coaches

```bash
curl -X GET http://localhost:8000/api/v1/auth/coaches \
  -H "Authorization: Bearer $TOKEN"
```

## 🛠️ CLI Commands

The project includes a command-line interface for administrative tasks.

### Available Commands

```bash
# Create AWS infrastructure (DynamoDB tables and S3 buckets)
python -m entrypoints.cli create-infra

# Create admin user
python -m entrypoints.cli create-admin \
    --email admin@example.com \
    --password Admin123! \
    --name "System Admin" \
    --phone "11999999999" \
    --dob "1990-01-01" \
    --nickname "admin"

# List all admin users
python -m entrypoints.cli list-admins
```

### Using as Installed Command

After installing the package, you can also use `servidor-cli`:

```bash
servidor-cli create-admin --email admin@example.com ...
```

See [CLI.md](CLI.md) for complete CLI documentation.

## 🚀 Deployment

### AWS Lambda Deployment

The application supports AWS Lambda deployment using the Mangum adapter.

**Lambda Configuration:**
- **Handler**: `entrypoints.lambda_handler.handler`
- **Runtime**: Python 3.11
- **Memory**: 512 MB (recommended)
- **Timeout**: 30 seconds (API Gateway max)
- **Environment Variables**: Same as `.env.example`

**Deployment Options:**

#### 1. AWS SAM

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ServidorAPI:
    Type: AWS::Serverless::Function
    Properties:
      Handler: entrypoints.lambda_handler.handler
      Runtime: python3.11
      CodeUri: .
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          AWS_ENDPOINT_URL: ""  # Empty for production
          SECRET_KEY: !Ref SecretKey
          STRAVA_CLIENT_ID: !Ref StravaClientId
          STRAVA_CLIENT_SECRET: !Ref StravaClientSecret
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

#### 2. Serverless Framework

```yaml
service: servidor-api

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  memorySize: 512
  timeout: 30
  environment:
    AWS_ENDPOINT_URL: ""
    SECRET_KEY: ${env:SECRET_KEY}
    STRAVA_CLIENT_ID: ${env:STRAVA_CLIENT_ID}
    STRAVA_CLIENT_SECRET: ${env:STRAVA_CLIENT_SECRET}

functions:
  api:
    handler: entrypoints.lambda_handler.handler
    events:
      - http:
          path: /
          method: ANY
      - http:
          path: /{proxy+}
          method: ANY
```

#### 3. AWS CDK (Python)

```python
from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    Stack, Duration
)

class ServidorStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Lambda Function
        api_lambda = lambda_.Function(
            self, "ServidorAPI",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="entrypoints.lambda_handler.handler",
            code=lambda_.Code.from_asset("."),
            memory_size=512,
            timeout=Duration.seconds(30),
            environment={
                "AWS_ENDPOINT_URL": "",
                "SECRET_KEY": "your-secret-key"
            }
        )
        
        # API Gateway
        api = apigw.LambdaRestApi(
            self, "ServidorEndpoint",
            handler=api_lambda,
            proxy=True
        )
```

### Docker Deployment

Build and run the Docker container:

```bash
# Build image
docker build -t servidor:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name servidor-api \
  servidor:latest
```

### Environment Variables for Production

Required environment variables for deployment:

```bash
# Application
APP_NAME=servidor
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security (CHANGE THESE!)
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS
AWS_REGION=us-east-1
AWS_ENDPOINT_URL=  # Empty for production

# DynamoDB Tables
DYNAMODB_USERS_TABLE=servidor-users-prod
DYNAMODB_TRAINING_PLANS_TABLE=servidor-training-plans-prod
DYNAMODB_ACTIVITIES_TABLE=servidor-activities-prod

# S3
S3_BUCKET_NAME=servidor-files-prod

# Strava (from https://www.strava.com/settings/api)
STRAVA_CLIENT_ID=your_production_client_id
STRAVA_CLIENT_SECRET=your_production_client_secret
STRAVA_WEBHOOK_VERIFY_TOKEN=your_webhook_token
STRAVA_CALLBACK_URL=https://your-domain.com/api/v1/strava/callback

# CORS
CORS_ORIGINS=["https://your-frontend.com"]
```

## ⚙️ Configuration

### Environment Variables

See `.env.example` for all configuration options. Key variables:

#### Application Settings
- `APP_NAME` - Application name
- `ENVIRONMENT` - Environment (local, staging, production)
- `DEBUG` - Debug mode (true/false)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

#### Security
- `SECRET_KEY` - JWT secret key (min 32 characters, **CHANGE IN PRODUCTION**)
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

#### AWS Configuration
- `AWS_REGION` - AWS region (default: us-east-1)
- `AWS_ACCESS_KEY_ID` - AWS access key (use "test" for LocalStack)
- `AWS_SECRET_ACCESS_KEY` - AWS secret key (use "test" for LocalStack)
- `AWS_ENDPOINT_URL` - AWS endpoint (http://localstack:4566 for local, empty for production)

#### DynamoDB Tables
- `DYNAMODB_USERS_TABLE` - Users table name
- `DYNAMODB_TRAINING_PLANS_TABLE` - Training plans table name
- `DYNAMODB_ACTIVITIES_TABLE` - Strava activities table name

#### S3 Storage
- `S3_BUCKET_NAME` - S3 bucket for file uploads

#### Strava Integration
- `STRAVA_CLIENT_ID` - Strava API client ID
- `STRAVA_CLIENT_SECRET` - Strava API client secret
- `STRAVA_WEBHOOK_VERIFY_TOKEN` - Webhook verification token
- `STRAVA_CALLBACK_URL` - OAuth callback URL

#### API Configuration
- `API_V1_PREFIX` - API version prefix (default: /api/v1)
- `CORS_ORIGINS` - Allowed CORS origins (JSON array)

## 🧪 Testing

### Run Tests

```bash
# Run all tests
make test

# Or directly with pytest
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Test Structure

```
tests/
├── unit/                   # Unit tests (pure logic)
│   ├── test_entities.py    # Domain entities
│   └── test_use_cases.py   # Use case logic
├── integration/            # Integration tests
│   ├── test_repositories.py # DynamoDB operations
│   └── test_api.py         # API endpoints
└── conftest.py            # Pytest fixtures
```

### Testing Strategy

- **Unit Tests**: Domain entities and use cases (mock repositories)
- **Integration Tests**: API endpoints with real DynamoDB (LocalStack)
- Use `pytest-asyncio` for async test support
- Mock external services (AWS, Strava API)

## 🏛️ Clean Architecture Benefits

### Why Clean Architecture?

1. **Independence from Frameworks**
   - Business logic doesn't depend on FastAPI, boto3, or other frameworks
   - Can switch frameworks without rewriting business rules

2. **Testability**
   - Easy to test use cases without external dependencies
   - Mock repositories for fast unit tests
   - Integration tests verify infrastructure

3. **Flexibility**
   - Change databases (DynamoDB → PostgreSQL) without touching domain
   - Swap authentication mechanisms without affecting business logic
   - Add new delivery mechanisms (GraphQL, gRPC) alongside REST

4. **Maintainability**
   - Clear boundaries and responsibilities
   - Changes in one layer don't affect others
   - Easy to understand and onboard new developers

5. **Scalability**
   - Add features without breaking existing code
   - Parallel development on different layers
   - Deploy to multiple targets (ASGI, Lambda) with same codebase

### Architecture Principles Applied

- **Dependency Inversion**: Inner layers define interfaces, outer layers implement them
- **Single Responsibility**: Each module has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Interface Segregation**: Specific interfaces over general ones
- **Dependency Rule**: Dependencies only point inward

## 🛣️ Roadmap

Future enhancements planned:

- [ ] Email notifications for training plan assignments
- [ ] Real-time chat between coaches and customers
- [ ] Training analytics and progress tracking
- [ ] Integration with other fitness platforms (Garmin, Polar)
- [ ] Payment processing for coach services
- [ ] Multi-language support

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Code Guidelines

1. **Follow Clean Architecture**
   - Keep domain layer pure (no external dependencies)
   - Use dependency injection for all services
   - Maintain clear layer boundaries

2. **Code Quality**
   - Write type hints for all functions
   - Add docstrings (Google style) for public functions
   - Follow PEP 8 style guide
   - Run tests before committing

3. **Testing**
   - Write unit tests for use cases
   - Add integration tests for API endpoints
   - Aim for >80% code coverage

4. **Documentation**
   - Update README if adding features
   - Document API changes in docstrings
   - Update ARCHITECTURE.md for structural changes

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📖 Additional Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide with examples
- [CLI.md](CLI.md) - CLI command reference
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

## 📊 Tech Stack

- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **Database**: AWS DynamoDB
- **Storage**: AWS S3
- **Authentication**: JWT (python-jose) + bcrypt
- **Dependency Injection**: dependency-injector
- **Validation**: Pydantic 2.5+
- **Testing**: pytest + pytest-asyncio
- **Package Manager**: UV (recommended) or pip
- **Containerization**: Docker + Docker Compose
- **Local AWS**: LocalStack
- **Lambda Adapter**: Mangum

## 📝 License

MIT License - see LICENSE file for details

## 👥 Authors

Built with ❤️ following Clean Architecture principles

## 🆘 Troubleshooting

### Common Issues

**Issue: LocalStack tables not created**
```bash
# Recreate infrastructure
python -m entrypoints.cli create-infra
```

**Issue: Port 8000 already in use**
```bash
# Check what's using the port
lsof -i :8000

# Kill the process or change the port
uvicorn entrypoints.asgi:app --port 8001
```

**Issue: JWT token invalid**
- Ensure `SECRET_KEY` in `.env` matches the one used to generate tokens
- Check token expiration time (default 30 minutes)
- Verify `Authorization: Bearer <token>` header format

**Issue: Strava callback not working**
- Verify `STRAVA_CALLBACK_URL` matches your Strava app settings
- Check that callback URL is accessible (use ngrok for local testing)
- Ensure `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET` are correct

**Issue: Docker container keeps restarting**
```bash
# Check logs
docker-compose logs api

# Check if LocalStack is ready
docker-compose logs localstack
```

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation
- Review closed issues for solutions

---

**Made with Clean Architecture** 🏗️ | **Powered by FastAPI** ⚡ | **Running on AWS** ☁️
