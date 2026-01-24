from enum import Enum


class UserType(str, Enum):
    """User type."""
    ADMIN = "admin"
    COACH = "coach"
    CUSTOMER = "customer"


class TrainingType(str, Enum):
    """Training type/method."""
    FARTLEK = "fartlek"
    LONG_RUN = "long_run"
    INTERVAL = "interval"
    TEMPO = "tempo"
    RECOVERY = "recovery"
    EASY_RUN = "easy_run"
    SPEED_WORK = "speed_work"
    HILL_REPEATS = "hill_repeats"
    THRESHOLD = "threshold"
    BASE_RUN = "base_run"


class TrainingZone(str, Enum):
    """Training intensity zone."""
    Z1 = "z1"  # Recovery
    Z2 = "z2"  # Easy/Aerobic
    Z3 = "z3"  # Moderate/Tempo
    Z4 = "z4"  # Threshold
    Z5 = "z5"  # VO2 Max
    Z6 = "z6"  # Anaerobic/Sprint


class TerrainType(str, Enum):
    """Terrain type."""
    FLAT = "flat"  # Plano
    HILL = "hill"  # Subida/Descida
    TRAIL = "trail"  # Trilha
    TRACK = "track"  # Pista
    MIXED = "mixed"  # Misto
    TREADMILL = "treadmill"  # Esteira


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


class ActivityMatchStatus(str, Enum):
    """Status of activity matching to training day."""
    MATCHED = "matched"
    UNMATCHED = "unmatched"
    IGNORED = "ignored"
