from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.domain.entities.enums import RunnerLevel, TrainingAvailability
import re


class UserBase(BaseModel):
    """Base schema for User."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=200, description="Full name")
    document_number: str = Field(..., description="CPF in format XXX.XXX.XXX-XX")
    date_of_birth: date = Field(..., description="Date of birth (minimum age: 16)")
    phone: str = Field(..., description="Phone number (11 digits)")
    nickname: Optional[str] = Field(None, max_length=100, description="Nickname or preferred name")
    runner_level: Optional[RunnerLevel] = Field(None, description="Runner experience level")
    training_availability: Optional[TrainingAvailability] = Field(None, description="Training frequency per week")
    challenge_next_month: Optional[str] = Field(None, max_length=500, description="Goal or challenge for next month")

    @field_validator('document_number')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Validate CPF format (XXX.XXX.XXX-XX)."""
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', v):
            raise ValueError('CPF must be in format XXX.XXX.XXX-XX')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number (11 digits only)."""
        if not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
        """Validate minimum age of 16 years."""
        from datetime import datetime
        today = datetime.now().date()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 16:
            raise ValueError('User must be at least 16 years old')
        return v


class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password (8-72 characters)")
    name: str = Field(..., min_length=1, max_length=200, description="Full name")
    document_number: str = Field(..., description="CPF in format XXX.XXX.XXX-XX")
    date_of_birth: date = Field(..., description="Date of birth (minimum age: 16)")
    phone: str = Field(..., description="Phone number (11 digits)")
    nickname: Optional[str] = Field(None, max_length=100, description="Nickname or preferred name")
    runner_level: Optional[RunnerLevel] = Field(None, description="Runner experience level")
    training_availability: Optional[TrainingAvailability] = Field(None, description="Training frequency per week")
    challenge_next_month: Optional[str] = Field(None, max_length=500, description="Goal or challenge for next month")

    @field_validator('document_number')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Validate CPF format (XXX.XXX.XXX-XX)."""
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', v):
            raise ValueError('CPF must be in format XXX.XXX.XXX-XX')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number (11 digits only)."""
        if not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
        """Validate minimum age of 16 years."""
        from datetime import datetime
        today = datetime.now().date()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 16:
            raise ValueError('User must be at least 16 years old')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "runner@example.com",
                "password": "securepass123",
                "name": "João Silva",
                "document_number": "123.456.789-00",
                "date_of_birth": "1995-06-15",
                "phone": "11987654321",
                "nickname": "João Runner",
                "runner_level": "intermediate",
                "training_availability": "3x",
                "challenge_next_month": "Run a 10K in under 50 minutes"
            }
        }


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
