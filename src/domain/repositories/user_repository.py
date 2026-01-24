from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.user import User


class UserRepository(ABC):
    """Repository interface for User entity."""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[User]:
        """List all users."""
        pass
