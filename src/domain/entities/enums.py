from enum import Enum


class RunnerLevel(str, Enum):
    """Runner experience level."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PRO = "pro"


class TrainingAvailability(str, Enum):
    """Training frequency per week."""
    ONE_TIME = "1x"
    TWO_TIMES = "2x"
    THREE_TIMES = "3x"
    FOUR_TIMES = "4x"
    FIVE_TIMES = "5x"
    SIX_TIMES = "6x"
    SEVEN_TIMES = "7x"
