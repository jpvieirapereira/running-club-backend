from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import date
from src.domain.entities.enums import RunnerLevel, TrainingAvailability


@dataclass
class UserDTO:
    """Data Transfer Object for User."""
    id: UUID
    email: str
    name: str
    document_number: str
    date_of_birth: date
    phone: str
    nickname: Optional[str]
    runner_level: Optional[RunnerLevel]
    training_availability: Optional[TrainingAvailability]
    challenge_next_month: Optional[str]
    is_active: bool


@dataclass
class CreateUserDTO:
    """DTO for creating a user."""
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
class LoginDTO:
    """DTO for user login."""
    email: str
    password: str


@dataclass
class TokenDTO:
    """DTO for authentication token."""
    access_token: str
    token_type: str = "bearer"
