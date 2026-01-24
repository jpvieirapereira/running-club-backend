"""
Admin repository interface.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.domain.entities.admin import Admin


class AdminRepository(ABC):
    """Repository interface for Admin users."""
    
    @abstractmethod
    async def create(self, admin: Admin) -> Admin:
        """
        Create a new admin.
        
        Args:
            admin: Admin to create
        
        Returns:
            Created admin
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, admin_id: UUID) -> Optional[Admin]:
        """
        Get admin by ID.
        
        Args:
            admin_id: Admin unique identifier
        
        Returns:
            Admin if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Admin]:
        """
        Get admin by email.
        
        Args:
            email: Admin email address
        
        Returns:
            Admin if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Admin]:
        """
        Get all admins.
        
        Returns:
            List of all admins
        """
        pass
    
    @abstractmethod
    async def update(self, admin: Admin) -> Admin:
        """
        Update an existing admin.
        
        Args:
            admin: Admin with updated data
        
        Returns:
            Updated admin
        """
        pass
    
    @abstractmethod
    async def delete(self, admin_id: UUID) -> bool:
        """
        Delete an admin.
        
        Args:
            admin_id: Admin unique identifier
        
        Returns:
            True if deleted, False if not found
        """
        pass
