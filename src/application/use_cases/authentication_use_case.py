from typing import Optional, Union
from uuid import UUID
from src.domain.entities.user import User
from src.domain.entities.coach import Coach
from src.domain.entities.customer import Customer
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.coach_repository import CoachRepository
from src.domain.repositories.customer_repository import CustomerRepository
from src.infrastructure.auth.auth_service import AuthService
from src.application.dtos import UserDTO, CoachDTO, CustomerDTO, LoginDTO, TokenDTO
from src.domain.entities.enums import UserType


class AuthenticationUseCase:
    """Use case for user authentication."""
    
    def __init__(
        self,
        coach_repository: CoachRepository,
        customer_repository: CustomerRepository,
        auth_service: AuthService
    ):
        self.coach_repository = coach_repository
        self.customer_repository = customer_repository
        self.auth_service = auth_service
    
    async def login(self, dto: LoginDTO) -> TokenDTO:
        """Authenticate user and return token."""
        # Try to find user as coach first
        user = await self.coach_repository.get_by_email(dto.email)
        user_type = UserType.COACH
        
        # If not found as coach, try customer
        if not user:
            user = await self.customer_repository.get_by_email(dto.email)
            user_type = UserType.CUSTOMER
        
        if not user or not self.auth_service.verify_password(dto.password, user.hashed_password):
            raise ValueError("Incorrect email or password")
        
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        access_token = self.auth_service.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "user_type": user_type.value
            }
        )
        
        return TokenDTO(access_token=access_token)
    
    async def get_current_user(self, token: str) -> Optional[Union[CoachDTO, CustomerDTO]]:
        """Get current user from token."""
        payload = self.auth_service.decode_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        user_type = payload.get("user_type")
        
        if not user_id:
            return None
        
        # Fetch user based on type
        if user_type == UserType.COACH.value:
            user = await self.coach_repository.get_by_id(UUID(user_id))
            if not user:
                return None
            return self._coach_to_dto(user)
        elif user_type == UserType.CUSTOMER.value:
            user = await self.customer_repository.get_by_id(UUID(user_id))
            if not user:
                return None
            return self._customer_to_dto(user)
        else:
            return None
    
    def _coach_to_dto(self, coach: Coach) -> CoachDTO:
        """Convert Coach entity to DTO."""
        return CoachDTO(
            id=coach.id,
            email=coach.email,
            name=coach.name,
            phone=coach.phone,
            date_of_birth=coach.date_of_birth,
            user_type=UserType.COACH,
            nickname=coach.nickname,
            is_active=coach.is_active,
            document_number=coach.document_number,
            bio=coach.bio,
            specialization=coach.specialization
        )
    
    def _customer_to_dto(self, customer: Customer) -> CustomerDTO:
        """Convert Customer entity to DTO."""
        return CustomerDTO(
            id=customer.id,
            email=customer.email,
            name=customer.name,
            phone=customer.phone,
            date_of_birth=customer.date_of_birth,
            user_type=UserType.CUSTOMER,
            nickname=customer.nickname,
            is_active=customer.is_active,
            document_number=customer.document_number,
            runner_level=customer.runner_level,
            training_availability=customer.training_availability,
            challenge_next_month=customer.challenge_next_month,
            coach_id=customer.coach_id
        )

