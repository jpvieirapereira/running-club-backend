from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.training_plan import TrainingPlan
from src.domain.entities.training_day import TrainingDay


class TrainingPlanRepository(ABC):
    """Repository interface for TrainingPlan entity."""
    
    @abstractmethod
    async def create(self, training_plan: TrainingPlan) -> TrainingPlan:
        """Create a new training plan."""
        pass
    
    @abstractmethod
    async def get_by_id(self, plan_id: UUID) -> Optional[TrainingPlan]:
        """Get training plan by ID with all training days."""
        pass
    
    @abstractmethod
    async def update(self, training_plan: TrainingPlan) -> TrainingPlan:
        """Update existing training plan."""
        pass
    
    @abstractmethod
    async def delete(self, plan_id: UUID) -> bool:
        """Delete training plan by ID."""
        pass
    
    @abstractmethod
    async def get_by_coach_id(self, coach_id: UUID) -> List[TrainingPlan]:
        """Get all training plans created by a coach."""
        pass
    
    @abstractmethod
    async def get_by_customer_id(self, customer_id: UUID) -> List[TrainingPlan]:
        """Get all training plans assigned to a customer."""
        pass
    
    @abstractmethod
    async def add_training_day(self, training_day: TrainingDay) -> TrainingDay:
        """Add a training day to a plan."""
        pass
    
    @abstractmethod
    async def update_training_day(self, training_day: TrainingDay) -> TrainingDay:
        """Update a training day."""
        pass
    
    @abstractmethod
    async def delete_training_day(self, training_day_id: UUID) -> bool:
        """Delete a training day."""
        pass
    
    @abstractmethod
    async def get_training_days(self, plan_id: UUID) -> List[TrainingDay]:
        """Get all training days for a plan."""
        pass
