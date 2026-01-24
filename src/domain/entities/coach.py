from typing import Optional
from uuid import UUID
from datetime import date
from src.domain.entities.user import User
from src.domain.entities.enums import UserType


class Coach(User):
    """Coach entity - can have multiple customers."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        name: str,
        phone: str,
        date_of_birth: date,
        document_number: str,  # CNPJ
        bio: Optional[str] = None,
        specialization: Optional[str] = None,
        nickname: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        super().__init__(
            email=email,
            hashed_password=hashed_password,
            name=name,
            phone=phone,
            date_of_birth=date_of_birth,
            user_type=UserType.COACH,
            nickname=nickname,
            is_active=is_active,
            id=id
        )
        self.document_number = document_number  # CNPJ
        self.bio = bio
        self.specialization = specialization
    
    def update_bio(self, bio: str):
        """Update coach bio."""
        self.bio = bio
    
    def update_specialization(self, specialization: str):
        """Update coach specialization."""
        self.specialization = specialization
