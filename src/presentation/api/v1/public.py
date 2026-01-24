from fastapi import APIRouter
from typing import List
from pydantic import BaseModel, Field
from src.domain.entities.enums import RunnerLevel, TrainingAvailability, TrainingType, TrainingZone, TerrainType


router = APIRouter(prefix="/public", tags=["Public"])


class EnumValue(BaseModel):
    """Schema for enum value."""
    value: str = Field(..., description="Enum value")
    label: str = Field(..., description="Human-readable label")


class EnumsResponse(BaseModel):
    """Schema for enums response."""
    runner_levels: List[EnumValue] = Field(..., description="Available runner experience levels")
    training_availabilities: List[EnumValue] = Field(..., description="Available training frequencies")
    training_types: List[EnumValue] = Field(..., description="Available training types")
    training_zones: List[EnumValue] = Field(..., description="Available training zones")
    terrain_types: List[EnumValue] = Field(..., description="Available terrain types")
    challenge_examples: List[str] = Field(..., description="Example challenges for inspiration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "runner_levels": [
                    {"value": "beginner", "label": "Beginner"},
                    {"value": "intermediate", "label": "Intermediate"}
                ],
                "training_types": [
                    {"value": "fartlek", "label": "Fartlek"},
                    {"value": "long_run", "label": "Long Run"}
                ],
                "training_zones": [
                    {"value": "z1", "label": "Z1 - Recovery"},
                    {"value": "z2", "label": "Z2 - Easy/Aerobic"}
                ],
                "terrain_types": [
                    {"value": "flat", "label": "Flat (Plano)"},
                    {"value": "hill", "label": "Hill"}
                ]
            }
        }


@router.get("/enums", response_model=EnumsResponse)
async def get_enums():
    """
    Get all valid enum values and examples.
    
    Returns available values for runner levels, training availabilities,
    training types, zones, terrains, and example challenges.
    
    This is a public endpoint - no authentication required.
    """
    # Map runner levels to human-readable labels
    runner_level_labels = {
        RunnerLevel.BEGINNER: "Beginner",
        RunnerLevel.INTERMEDIATE: "Intermediate",
        RunnerLevel.ADVANCED: "Advanced",
        RunnerLevel.PRO: "Professional"
    }
    
    # Map training availability to human-readable labels
    training_availability_labels = {
        TrainingAvailability.ONE_TIME: "1x per week",
        TrainingAvailability.TWO_TIMES: "2x per week",
        TrainingAvailability.THREE_TIMES: "3x per week",
        TrainingAvailability.FOUR_TIMES: "4x per week",
        TrainingAvailability.FIVE_TIMES: "5x per week",
        TrainingAvailability.SIX_TIMES: "6x per week",
        TrainingAvailability.SEVEN_TIMES: "7x per week (daily)"
    }
    
    # Map training types to human-readable labels
    training_type_labels = {
        TrainingType.FARTLEK: "Fartlek",
        TrainingType.LONG_RUN: "Long Run",
        TrainingType.INTERVAL: "Interval Training",
        TrainingType.TEMPO: "Tempo Run",
        TrainingType.RECOVERY: "Recovery Run",
        TrainingType.EASY_RUN: "Easy Run",
        TrainingType.SPEED_WORK: "Speed Work",
        TrainingType.HILL_REPEATS: "Hill Repeats",
        TrainingType.THRESHOLD: "Threshold Run",
        TrainingType.BASE_RUN: "Base Run"
    }
    
    # Map training zones to human-readable labels
    training_zone_labels = {
        TrainingZone.Z1: "Z1 - Recovery",
        TrainingZone.Z2: "Z2 - Easy/Aerobic",
        TrainingZone.Z3: "Z3 - Moderate/Tempo",
        TrainingZone.Z4: "Z4 - Threshold",
        TrainingZone.Z5: "Z5 - VO2 Max",
        TrainingZone.Z6: "Z6 - Anaerobic/Sprint"
    }
    
    # Map terrain types to human-readable labels
    terrain_type_labels = {
        TerrainType.FLAT: "Flat (Plano)",
        TerrainType.HILL: "Hill (Subida)",
        TerrainType.TRAIL: "Trail (Trilha)",
        TerrainType.TRACK: "Track (Pista)",
        TerrainType.MIXED: "Mixed (Misto)",
        TerrainType.TREADMILL: "Treadmill (Esteira)"
    }
    
    # Example challenges for inspiration
    challenge_examples = [
        "Run a 5K in under 30 minutes",
        "Complete a 10K race",
        "Run a half marathon (21K)",
        "Complete a full marathon (42K)",
        "Improve my pace by 30 seconds per km",
        "Run 100km in total this month",
        "Run 3 times per week consistently",
        "Participate in a local running event",
        "Beat my personal record in 5K",
        "Run my first trail race"
    ]
    
    return EnumsResponse(
        runner_levels=[
            EnumValue(value=level.value, label=runner_level_labels[level])
            for level in RunnerLevel
        ],
        training_availabilities=[
            EnumValue(value=availability.value, label=training_availability_labels[availability])
            for availability in TrainingAvailability
        ],
        training_types=[
            EnumValue(value=ttype.value, label=training_type_labels[ttype])
            for ttype in TrainingType
        ],
        training_zones=[
            EnumValue(value=zone.value, label=training_zone_labels[zone])
            for zone in TrainingZone
        ],
        terrain_types=[
            EnumValue(value=terrain.value, label=terrain_type_labels[terrain])
            for terrain in TerrainType
        ],
        challenge_examples=challenge_examples
    )

