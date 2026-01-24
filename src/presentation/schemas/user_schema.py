from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base schema for User."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str
