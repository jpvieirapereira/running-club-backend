from typing import Optional
from uuid import UUID
from datetime import date, datetime
from src.domain.entities.user import User
from src.domain.entities.enums import UserType, RunnerLevel, TrainingAvailability


class Customer(User):
    """Customer entity - runner who can have one coach."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        name: str,
        phone: str,
        date_of_birth: date,
        document_number: str,  # CPF
        runner_level: Optional[RunnerLevel] = None,
        training_availability: Optional[TrainingAvailability] = None,
        challenge_next_month: Optional[str] = None,
        coach_id: Optional[UUID] = None,
        strava_athlete_id: Optional[int] = None,
        strava_connected_at: Optional[datetime] = None,
        strava_last_sync: Optional[datetime] = None,
        nickname: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        super().__init__(
            email=email,
            hashed_password=hashed_password,
            name=name,
            phone=phone,
            date_of_birth=date_of_birth,
            user_type=UserType.CUSTOMER,
            nickname=nickname,
            is_active=is_active,
            id=id
        )
        self.document_number = document_number  # CPF
        self.runner_level = runner_level
        self.training_availability = training_availability
        self.challenge_next_month = challenge_next_month
        self.coach_id = coach_id
        self.strava_athlete_id = strava_athlete_id
        self.strava_connected_at = strava_connected_at
        self.strava_last_sync = strava_last_sync
    
    def assign_coach(self, coach_id: UUID):
        """Assign a coach to this customer."""
        self.coach_id = coach_id
    
    def remove_coach(self):
        """Remove coach assignment."""
        self.coach_id = None
    
    def update_training_goal(self, challenge: str):
        """Update training challenge/goal."""
        self.challenge_next_month = challenge
    
    def connect_strava(self, athlete_id: int) -> None:
        """
        Connect Strava account.
        
        Args:
            athlete_id: Strava athlete ID
        """
        self.strava_athlete_id = athlete_id
        self.strava_connected_at = datetime.utcnow()
    
    def disconnect_strava(self) -> None:
        """Disconnect Strava account."""
        self.strava_athlete_id = None
        self.strava_connected_at = None
        self.strava_last_sync = None
    
    def update_last_sync(self) -> None:
        """Update last Strava sync timestamp."""
        self.strava_last_sync = datetime.utcnow()
    
    def is_strava_connected(self) -> bool:
        """Check if Strava is connected."""
        return self.strava_athlete_id is not None
