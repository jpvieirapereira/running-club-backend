from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID
from datetime import date
from src.domain.entities.enums import TrainingType, TrainingZone, TerrainType


@dataclass
class TrainingDayDTO:
    """Data Transfer Object for TrainingDay."""
    id: UUID
    training_plan_id: UUID
    date: date
    training_type: TrainingType
    zone: TrainingZone
    terrain: TerrainType
    distance_km: float
    workout_details: str
    day_order: int


@dataclass
class CreateTrainingDayDTO:
    """DTO for creating a training day."""
    date: date
    training_type: TrainingType
    zone: TrainingZone
    terrain: TerrainType
    distance_km: float
    workout_details: str
    day_order: int = 1


@dataclass
class UpdateTrainingDayDTO:
    """DTO for updating a training day."""
    training_type: Optional[TrainingType] = None
    zone: Optional[TrainingZone] = None
    terrain: Optional[TerrainType] = None
    distance_km: Optional[float] = None
    workout_details: Optional[str] = None


@dataclass
class TrainingPlanDTO:
    """Data Transfer Object for TrainingPlan."""
    id: UUID
    coach_id: UUID
    customer_id: UUID
    name: str
    start_date: date
    end_date: date
    description: Optional[str]
    success_criteria: Optional[str]
    is_active: bool
    training_days: List[TrainingDayDTO]


@dataclass
class CreateTrainingPlanDTO:
    """DTO for creating a training plan."""
    customer_id: UUID
    name: str
    start_date: date
    end_date: date
    description: Optional[str] = None
    success_criteria: Optional[str] = None
    training_days: List[CreateTrainingDayDTO] = None


@dataclass
class UpdateTrainingPlanDTO:
    """DTO for updating a training plan."""
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    success_criteria: Optional[str] = None
