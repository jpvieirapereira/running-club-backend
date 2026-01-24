from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.domain.entities.enums import RunnerLevel, TrainingAvailability, UserType
import re


class UserBase(BaseModel):
    """Base schema for User."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=200, description="Full name")
    phone: str = Field(..., description="Phone number (11 digits)")
    date_of_birth: date = Field(..., description="Date of birth (minimum age: 16)")
    nickname: Optional[str] = Field(None, max_length=100, description="Nickname or preferred name")

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


class CoachCreate(BaseModel):
    """Schema for creating a coach."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password (8-72 characters)")
    name: str = Field(..., min_length=1, max_length=200, description="Full name")
    phone: str = Field(..., description="Phone number (11 digits)")
    date_of_birth: date = Field(..., description="Date of birth (minimum age: 16)")
    document_number: str = Field(..., description="CNPJ in format XX.XXX.XXX/XXXX-XX")
    bio: Optional[str] = Field(None, max_length=1000, description="Coach bio")
    specialization: Optional[str] = Field(None, max_length=200, description="Coach specialization")
    nickname: Optional[str] = Field(None, max_length=100, description="Nickname")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v
    
    @field_validator('document_number')
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        """Validate CNPJ format."""
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', v):
            raise ValueError('CNPJ must be in format XX.XXX.XXX/XXXX-XX')
        return v
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
        from datetime import datetime
        today = datetime.now().date()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 16:
            raise ValueError('User must be at least 16 years old')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "coach@example.com",
                "password": "securepass123",
                "name": "Maria Silva",
                "phone": "11987654321",
                "date_of_birth": "1985-03-20",
                "document_number": "12.345.678/0001-90",
                "bio": "Experienced running coach with 10 years of experience",
                "specialization": "Marathon Training",
                "nickname": "Coach Maria"
            }
        }


class CustomerCreate(BaseModel):
    """Schema for creating a customer."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password (8-72 characters)")
    name: str = Field(..., min_length=1, max_length=200, description="Full name")
    phone: str = Field(..., description="Phone number (11 digits)")
    date_of_birth: date = Field(..., description="Date of birth (minimum age: 16)")
    document_number: str = Field(..., description="CPF in format XXX.XXX.XXX-XX")
    runner_level: Optional[RunnerLevel] = Field(None, description="Runner experience level")
    training_availability: Optional[TrainingAvailability] = Field(None, description="Training frequency per week")
    challenge_next_month: Optional[str] = Field(None, max_length=500, description="Goal or challenge for next month")
    nickname: Optional[str] = Field(None, max_length=100, description="Nickname")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v
    
    @field_validator('document_number')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Validate CPF format (XXX.XXX.XXX-XX)."""
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', v):
            raise ValueError('CPF must be in format XXX.XXX.XXX-XX')
        return v
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
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
                "phone": "11987654321",
                "date_of_birth": "1995-06-15",
                "document_number": "123.456.789-00",
                "runner_level": "intermediate",
                "training_availability": "3x",
                "challenge_next_month": "Run a 10K in under 50 minutes",
                "nickname": "João Runner"
            }
        }


class CoachUpdate(BaseModel):
    """Schema for updating coach profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, description="Phone number (11 digits)")
    nickname: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    specialization: Optional[str] = Field(None, max_length=200)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v


class CustomerUpdate(BaseModel):
    """Schema for updating customer profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, description="Phone number (11 digits)")
    nickname: Optional[str] = Field(None, max_length=100)
    runner_level: Optional[RunnerLevel] = None
    training_availability: Optional[TrainingAvailability] = None
    challenge_next_month: Optional[str] = Field(None, max_length=500)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v


class CoachResponse(BaseModel):
    """Schema for coach response."""
    id: UUID
    email: EmailStr
    name: str
    phone: str
    date_of_birth: date
    document_number: str
    user_type: UserType
    nickname: Optional[str]
    bio: Optional[str]
    specialization: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


class CustomerResponse(BaseModel):
    """Schema for customer response."""
    id: UUID
    email: EmailStr
    name: str
    phone: str
    date_of_birth: date
    document_number: str
    user_type: UserType
    nickname: Optional[str]
    runner_level: Optional[RunnerLevel]
    training_availability: Optional[TrainingAvailability]
    challenge_next_month: Optional[str]
    coach_id: Optional[UUID]
    is_active: bool
    
    class Config:
        from_attributes = True


class AssignCoach(BaseModel):
    """Schema for assigning coach to customer."""
    customer_id: UUID = Field(..., description="Customer ID to assign")


# Legacy schemas - keeping for backward compatibility
class UserCreate(BaseModel):
    """Schema for creating a user (legacy - use CustomerCreate instead)."""
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


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Full name")
    phone: Optional[str] = Field(None, description="Phone number (11 digits)")
    nickname: Optional[str] = Field(None, max_length=100, description="Nickname or preferred name")
    runner_level: Optional[RunnerLevel] = Field(None, description="Runner experience level")
    training_availability: Optional[TrainingAvailability] = Field(None, description="Training frequency per week")
    challenge_next_month: Optional[str] = Field(None, max_length=500, description="Goal or challenge for next month")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number (11 digits only)."""
        if v is not None and not re.match(r'^\d{11}$', v):
            raise ValueError('Phone must contain exactly 11 digits')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva Updated",
                "phone": "11987654321",
                "nickname": "João Runner Pro",
                "runner_level": "advanced",
                "training_availability": "5x",
                "challenge_next_month": "Run a half marathon"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (legacy)."""
    id: UUID
    email: EmailStr
    name: str
    phone: str
    date_of_birth: date
    document_number: str
    user_type: UserType
    nickname: Optional[str]
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

