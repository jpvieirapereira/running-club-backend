"""
Admin entity.
"""
from typing import Optional
from uuid import UUID
from datetime import date
from src.domain.entities.user import User
from src.domain.entities.enums import UserType


class Admin(User):
    """Admin entity - system administrator with full permissions."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        name: str,
        phone: str,
        date_of_birth: date,
        nickname: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        """
        Initialize an Admin user.
        
        Args:
            email: Admin email address
            hashed_password: Hashed password
            name: Admin full name
            phone: Admin phone number
            date_of_birth: Admin date of birth
            nickname: Optional nickname
            is_active: Whether admin account is active
            id: Unique identifier (auto-generated if not provided)
        """
        super().__init__(
            email=email,
            hashed_password=hashed_password,
            name=name,
            phone=phone,
            date_of_birth=date_of_birth,
            user_type=UserType.ADMIN,
            nickname=nickname,
            is_active=is_active,
            id=id
        )
