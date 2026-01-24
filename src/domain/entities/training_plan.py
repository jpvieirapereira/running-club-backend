from typing import Optional, List
from uuid import UUID
from datetime import date
from src.domain.entities.base import Entity
from src.domain.entities.training_day import TrainingDay


class TrainingPlan(Entity):
    """Training plan entity - a plan assigned by coach to customer."""
    
    def __init__(
        self,
        coach_id: UUID,
        customer_id: UUID,
        name: str,
        start_date: date,
        end_date: date,
        description: Optional[str] = None,
        success_criteria: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self.coach_id = coach_id
        self.customer_id = customer_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.success_criteria = success_criteria
        self.is_active = is_active
        self.training_days: List[TrainingDay] = []
    
    def add_training_day(self, training_day: TrainingDay):
        """Add a training day to the plan."""
        if training_day.training_plan_id != self.id:
            raise ValueError("Training day does not belong to this plan")
        self.training_days.append(training_day)
    
    def remove_training_day(self, training_day_id: UUID):
        """Remove a training day from the plan."""
        self.training_days = [
            day for day in self.training_days 
            if day.id != training_day_id
        ]
    
    def deactivate(self):
        """Deactivate the training plan."""
        self.is_active = False
    
    def activate(self):
        """Activate the training plan."""
        self.is_active = True
    
    def update_info(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        success_criteria: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ):
        """Update plan information."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if success_criteria is not None:
            self.success_criteria = success_criteria
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
