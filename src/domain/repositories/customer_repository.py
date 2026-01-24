from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.customer import Customer


class CustomerRepository(ABC):
    """Repository interface for Customer entity."""
    
    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        """Create a new customer."""
        pass
    
    @abstractmethod
    async def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """Get customer by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        pass
    
    @abstractmethod
    async def update(self, customer: Customer) -> Customer:
        """Update existing customer."""
        pass
    
    @abstractmethod
    async def delete(self, customer_id: UUID) -> bool:
        """Delete customer by ID."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Customer]:
        """List all customers."""
        pass
    
    @abstractmethod
    async def get_by_coach_id(self, coach_id: UUID) -> List[Customer]:
        """Get all customers assigned to a coach."""
        pass
    
    @abstractmethod
    async def get_by_document_number(self, document_number: str) -> Optional[Customer]:
        """Get customer by CPF."""
        pass
