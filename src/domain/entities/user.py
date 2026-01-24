from typing import Optional
from uuid import UUID
from datetime import date
from abc import abstractmethod
from src.domain.entities.base import Entity
from src.domain.entities.enums import UserType


class User(Entity):
    """Abstract base user entity."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        name: str,
        phone: str,
        date_of_birth: date,
        user_type: UserType,
        nickname: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self.email = email
        self.hashed_password = hashed_password
        self.name = name
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.user_type = user_type
        self.nickname = nickname
        self.is_active = is_active
    
    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
    
    def activate(self):
        """Activate user account."""
        self.is_active = True

