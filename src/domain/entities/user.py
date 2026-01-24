from typing import Optional
from uuid import UUID
from datetime import date
from src.domain.entities.base import Entity
from src.domain.entities.enums import RunnerLevel, TrainingAvailability


class User(Entity):
    """User domain entity for running/training application."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        name: str,
        document_number: str,
        date_of_birth: date,
        phone: str,
        nickname: Optional[str] = None,
        runner_level: Optional[RunnerLevel] = None,
        training_availability: Optional[TrainingAvailability] = None,
        challenge_next_month: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self.email = email
        self.hashed_password = hashed_password
        self.name = name
        self.document_number = document_number
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.nickname = nickname
        self.runner_level = runner_level
        self.training_availability = training_availability
        self.challenge_next_month = challenge_next_month
        self.is_active = is_active
    
    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
    
    def activate(self):
        """Activate user account."""
        self.is_active = True
