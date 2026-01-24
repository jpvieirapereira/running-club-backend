from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.coach import Coach


class CoachRepository(ABC):
    """Repository interface for Coach entity."""
    
    @abstractmethod
    async def create(self, coach: Coach) -> Coach:
        """Create a new coach."""
        pass
    
    @abstractmethod
    async def get_by_id(self, coach_id: UUID) -> Optional[Coach]:
        """Get coach by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Coach]:
        """Get coach by email."""
        pass
    
    @abstractmethod
    async def update(self, coach: Coach) -> Coach:
        """Update existing coach."""
        pass
    
    @abstractmethod
    async def delete(self, coach_id: UUID) -> bool:
        """Delete coach by ID."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Coach]:
        """List all coaches."""
        pass
    
    @abstractmethod
    async def get_by_document_number(self, document_number: str) -> Optional[Coach]:
        """Get coach by CNPJ."""
        pass
