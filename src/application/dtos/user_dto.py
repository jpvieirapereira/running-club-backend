from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import date
from src.domain.entities.enums import RunnerLevel, TrainingAvailability, UserType


@dataclass
class UserDTO:
    """Base Data Transfer Object for User."""
    id: UUID
    email: str
    name: str
    phone: str
    date_of_birth: date
    user_type: UserType
    nickname: Optional[str]
    is_active: bool


@dataclass
class CoachDTO(UserDTO):
    """Data Transfer Object for Coach."""
    document_number: str  # CNPJ
    bio: Optional[str] = None
    specialization: Optional[str] = None


@dataclass
class CustomerDTO(UserDTO):
    """Data Transfer Object for Customer."""
    document_number: str  # CPF
    runner_level: Optional[RunnerLevel] = None
    training_availability: Optional[TrainingAvailability] = None
    challenge_next_month: Optional[str] = None
    coach_id: Optional[UUID] = None


@dataclass
class AdminDTO(UserDTO):
    """Data Transfer Object for Admin."""
    pass


@dataclass
class CreateCoachDTO:
    """DTO for creating a coach."""
    email: str
    password: str
    name: str
    phone: str
    date_of_birth: date
    document_number: str  # CNPJ
    bio: Optional[str] = None
    specialization: Optional[str] = None
    nickname: Optional[str] = None


@dataclass
class CreateCustomerDTO:
    """DTO for creating a customer."""
    email: str
    password: str
    name: str
    phone: str
    date_of_birth: date
    document_number: str  # CPF
    runner_level: Optional[RunnerLevel] = None
    training_availability: Optional[TrainingAvailability] = None
    challenge_next_month: Optional[str] = None
    nickname: Optional[str] = None


@dataclass
class CreateAdminDTO:
    """DTO for creating an admin."""
    email: str
    password: str
    name: str
    phone: str
    date_of_birth: date
    nickname: Optional[str] = None


@dataclass
class CreateUserDTO:
    """DTO for creating a user (legacy - to be removed)."""
    email: str
    password: str
    name: str
    document_number: str
    date_of_birth: date
    phone: str
    nickname: Optional[str] = None
    runner_level: Optional[RunnerLevel] = None
    training_availability: Optional[TrainingAvailability] = None
    challenge_next_month: Optional[str] = None


@dataclass
class UpdateCoachDTO:
    """DTO for updating coach profile."""
    name: Optional[str] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    bio: Optional[str] = None
    specialization: Optional[str] = None


@dataclass
class UpdateCustomerDTO:
    """DTO for updating customer profile."""
    name: Optional[str] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    runner_level: Optional[RunnerLevel] = None
    training_availability: Optional[TrainingAvailability] = None
    challenge_next_month: Optional[str] = None


@dataclass
class UpdateUserDTO:
    """DTO for updating user profile (legacy)."""
    name: Optional[str] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    runner_level: Optional[RunnerLevel] = None
    training_availability: Optional[TrainingAvailability] = None
    challenge_next_month: Optional[str] = None


@dataclass
class AssignCoachDTO:
    """DTO for assigning a coach to a customer."""
    customer_id: UUID
    coach_id: UUID


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

