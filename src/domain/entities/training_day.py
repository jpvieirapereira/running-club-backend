from typing import Optional
from uuid import UUID
from datetime import date
from src.domain.entities.base import Entity
from src.domain.entities.enums import TrainingType, TrainingZone, TerrainType


class TrainingDay(Entity):
    """Training day entity - represents a single workout in a training plan."""
    
    def __init__(
        self,
        training_plan_id: UUID,
        date: date,
        training_type: TrainingType,
        zone: TrainingZone,
        terrain: TerrainType,
        distance_km: float,
        workout_details: str,
        day_order: int = 1,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self.training_plan_id = training_plan_id
        self.date = date
        self.training_type = training_type
        self.zone = zone
        self.terrain = terrain
        self.distance_km = distance_km
        self.workout_details = workout_details
        self.day_order = day_order
    
    def update_workout(
        self,
        training_type: Optional[TrainingType] = None,
        zone: Optional[TrainingZone] = None,
        terrain: Optional[TerrainType] = None,
        distance_km: Optional[float] = None,
        workout_details: Optional[str] = None
    ):
        """Update workout details."""
        if training_type is not None:
            self.training_type = training_type
        if zone is not None:
            self.zone = zone
        if terrain is not None:
            self.terrain = terrain
        if distance_km is not None:
            self.distance_km = distance_km
        if workout_details is not None:
            self.workout_details = workout_details
