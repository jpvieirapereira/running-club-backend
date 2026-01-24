# Servidor CLI

Command-line interface for administrative tasks.

## Installation

```bash
# Install dependencies
pip install -e .

# Or with uv
uv pip install -e .
```

After installation, you can use either:
- `python -m entrypoints.cli` 
- `servidor-cli` (installed command)

## Commands

### create-admin

Create a new admin user.

```bash
# Using module
python -m entrypoints.cli create-admin \
    --email admin@example.com \
    --password SecureP@ss123 \
    --name "John Admin" \
    --phone "11999999999" \
    --dob "1990-01-01"

# Using installed command
servidor-cli create-admin \
    --email admin@example.com \
    --password SecureP@ss123 \
    --name "John Admin" \
    --phone "11999999999" \
    --dob "1990-01-01"
```

**Options:**
- `--email, -e` - Admin email (required)
- `--password, -p` - Admin password (required)
- `--name, -n` - Full name (required)
- `--phone` - Phone number (required)
- `--dob` - Date of birth in YYYY-MM-DD format (required)
- `--nickname` - Optional nickname

### create-infra

Create AWS infrastructure (DynamoDB tables and S3 buckets).

```bash
# Create everything
servidor-cli create-infra

# Create only DynamoDB tables
servidor-cli create-infra --no-buckets

# Create only S3 buckets
servidor-cli create-infra --no-tables
```

**Creates:**
- DynamoDB tables: users, tasks, training_plans, strava_activities
- S3 bucket: servidor-files

**Note:** Safe to run multiple times - handles existing resources gracefully.

### list-admins

List all admin users.

```bash
servidor-cli list-admins
```

## Usage Examples

### First-time Setup

```bash
# 1. Start LocalStack (if using local development)
docker-compose up -d

# 2. Create infrastructure
servidor-cli create-infra

# 3. Create first admin
servidor-cli create-admin \
    --email admin@servidor.com \
    --password Admin@123 \
    --name "System Administrator" \
    --phone "11999999999" \
    --dob "1990-01-01"

# 4. Verify
servidor-cli list-admins
```

### Production Setup

```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
export AWS_ENDPOINT_URL=  # Leave empty for real AWS

# Create infrastructure
servidor-cli create-infra

# Create admin
servidor-cli create-admin \
    --email admin@yourdomain.com \
    --password <secure-password> \
    --name "Production Admin" \
    --phone "11999999999" \
    --dob "1990-01-01"
```

## Help

Get help for any command:

```bash
servidor-cli --help
servidor-cli create-admin --help
servidor-cli create-infra --help
servidor-cli list-admins --help
```

## Configuration

The CLI uses the same configuration as the main application from `src/infrastructure/config/settings.py`:

- `DYNAMODB_USERS_TABLE` - Users table name (default: "users")
- `DYNAMODB_TASKS_TABLE` - Tasks table name (default: "tasks")
- `DYNAMODB_TRAINING_PLANS_TABLE` - Training plans table (default: "training_plans")
- `DYNAMODB_ACTIVITIES_TABLE` - Activities table (default: "strava_activities")
- `S3_BUCKET_NAME` - S3 bucket name (default: "servidor-files")
- `AWS_ENDPOINT_URL` - AWS endpoint (default: "http://localhost:4566" for LocalStack)
- `AWS_REGION` - AWS region (default: "us-east-1")

Set via environment variables or `.env` file.

## Troubleshooting

### "ModuleNotFoundError: No module named 'typer'"

Install dependencies:
```bash
pip install -e .
```

### "Unable to locate credentials"

For LocalStack (local development), the default test credentials work.

For AWS, set your credentials:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### "ResourceInUseException: Table already exists"

This is normal - the CLI handles existing resources. The table will be skipped with a yellow warning message.

### "Admin with email X already exists"

Email addresses must be unique. Use a different email or delete the existing admin first.

## Architecture

The CLI follows Clean Architecture principles:
- Uses domain entities (Admin, User)
- Uses application use cases (AdminUseCase)
- Uses infrastructure repositories (DynamoDBAdminRepository)
- Uses dependency injection (Container)

This ensures consistency with the web API and maintains separation of concerns.
