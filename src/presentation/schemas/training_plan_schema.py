from typing import Optional, List
from uuid import UUID
from datetime import date as date_type
from pydantic import BaseModel, Field
from src.domain.entities.enums import TrainingType, TrainingZone, TerrainType


class TrainingDayBase(BaseModel):
    """Base schema for TrainingDay."""
    date: date_type = Field(..., description="Date of the training")
    training_type: TrainingType = Field(..., description="Type of training")
    zone: TrainingZone = Field(..., description="Training intensity zone")
    terrain: TerrainType = Field(..., description="Terrain type")
    distance_km: float = Field(..., gt=0, description="Distance in kilometers")
    workout_details: str = Field(..., max_length=500, description="Workout details (e.g., '4x 500m(z3)/ 500m(z4)')")
    day_order: int = Field(default=1, ge=1, description="Order/sequence within the day")


class TrainingDayCreate(TrainingDayBase):
    """Schema for creating a training day."""
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-02-15",
                "training_type": "fartlek",
                "zone": "z4",
                "terrain": "flat",
                "distance_km": 8.0,
                "workout_details": "4x 500m(z3)/ 500m(z4)",
                "day_order": 1
            }
        }


class TrainingDayUpdate(BaseModel):
    """Schema for updating a training day."""
    training_type: Optional[TrainingType] = None
    zone: Optional[TrainingZone] = None
    terrain: Optional[TerrainType] = None
    distance_km: Optional[float] = Field(None, gt=0)
    workout_details: Optional[str] = Field(None, max_length=500)


class TrainingDayResponse(TrainingDayBase):
    """Schema for training day response."""
    id: UUID
    training_plan_id: UUID
    
    class Config:
        from_attributes = True


class TrainingPlanCreate(BaseModel):
    """Schema for creating a training plan."""
    customer_id: UUID = Field(..., description="Customer to assign the plan to")
    name: str = Field(..., min_length=1, max_length=200, description="Plan name")
    start_date: date_type = Field(..., description="Plan start date")
    end_date: date_type = Field(..., description="Plan end date")
    description: Optional[str] = Field(None, max_length=1000, description="Plan description")
    success_criteria: Optional[str] = Field(None, max_length=500, description="Success goal/criteria")
    training_days: Optional[List[TrainingDayCreate]] = Field(default=[], description="Training days in the plan")
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "uuid-of-customer",
                "name": "Marathon Preparation - February",
                "start_date": "2024-02-01",
                "end_date": "2024-02-28",
                "description": "4-week marathon preparation plan",
                "success_criteria": "Complete a marathon in under 4 hours",
                "training_days": [
                    {
                        "date": "2024-02-01",
                        "training_type": "easy_run",
                        "zone": "z2",
                        "terrain": "flat",
                        "distance_km": 10.0,
                        "workout_details": "Easy recovery run",
                        "day_order": 1
                    }
                ]
            }
        }


class TrainingPlanUpdate(BaseModel):
    """Schema for updating a training plan."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[date_type] = None
    end_date: Optional[date_type] = None
    description: Optional[str] = Field(None, max_length=1000)
    success_criteria: Optional[str] = Field(None, max_length=500)


class TrainingPlanResponse(BaseModel):
    """Schema for training plan response."""
    id: UUID
    coach_id: UUID
    customer_id: UUID
    name: str
    start_date: date_type
    end_date: date_type
    description: Optional[str]
    success_criteria: Optional[str]
    is_active: bool
    training_days: List[TrainingDayResponse]
    
    class Config:
        from_attributes = True
