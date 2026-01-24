from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserDTO:
    """Data Transfer Object for User."""
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool


@dataclass
class CreateUserDTO:
    """DTO for creating a user."""
    email: str
    password: str
    full_name: Optional[str] = None


@dataclass
class LoginDTO:
    """DTO for user login."""
    email: str
    password: str


@dataclass
class TokenDTO:
    """DTO for authentication token."""
    access_token: str
    token_type: str = "bearer"
