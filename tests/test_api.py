import pytest
from httpx import AsyncClient
from src.presentation.api.app import create_app


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    return create_app()


@pytest.fixture
async def client(app):
    """Create async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_register_user(client):
    """Test user registration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "document_number": "123.456.789-00",
            "date_of_birth": "1995-06-15",
            "phone": "11987654321",
            "nickname": "Tester",
            "runner_level": "beginner",
            "training_availability": "3x",
            "challenge_next_month": "Run 5K"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["document_number"] == "123.456.789-00"
    assert "id" in data
