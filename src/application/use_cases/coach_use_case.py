from typing import List
from uuid import UUID
from src.domain.entities.coach import Coach
from src.domain.repositories.coach_repository import CoachRepository
from src.domain.repositories.customer_repository import CustomerRepository
from src.infrastructure.auth.auth_service import AuthService
from src.application.dtos import CoachDTO, CreateCoachDTO, UpdateCoachDTO, CustomerDTO, AssignCoachDTO


class CoachUseCase:
    """Use case for coach operations."""
    
    def __init__(
        self,
        coach_repository: CoachRepository,
        customer_repository: CustomerRepository,
        auth_service: AuthService
    ):
        self.coach_repository = coach_repository
        self.customer_repository = customer_repository
        self.auth_service = auth_service
    
    async def register(self, dto: CreateCoachDTO) -> CoachDTO:
        """Register a new coach."""
        # Check if email already exists
        existing_coach = await self.coach_repository.get_by_email(dto.email)
        if existing_coach:
            raise ValueError("User with this email already exists")
        
        # Check if CNPJ already exists
        existing_by_doc = await self.coach_repository.get_by_document_number(dto.document_number)
        if existing_by_doc:
            raise ValueError("CNPJ already registered")
        
        # Create new coach
        hashed_password = self.auth_service.get_password_hash(dto.password)
        coach = Coach(
            email=dto.email,
            hashed_password=hashed_password,
            name=dto.name,
            phone=dto.phone,
            date_of_birth=dto.date_of_birth,
            document_number=dto.document_number,
            bio=dto.bio,
            specialization=dto.specialization,
            nickname=dto.nickname
        )
        
        created_coach = await self.coach_repository.create(coach)
        
        return self._to_dto(created_coach)
    
    async def update_profile(self, coach_id: UUID, dto: UpdateCoachDTO) -> CoachDTO:
        """Update coach profile."""
        coach = await self.coach_repository.get_by_id(coach_id)
        if not coach:
            raise ValueError("Coach not found")
        
        # Update only provided fields
        if dto.name is not None:
            coach.name = dto.name
        if dto.phone is not None:
            coach.phone = dto.phone
        if dto.nickname is not None:
            coach.nickname = dto.nickname
        if dto.bio is not None:
            coach.bio = dto.bio
        if dto.specialization is not None:
            coach.specialization = dto.specialization
        
        updated_coach = await self.coach_repository.update(coach)
        
        return self._to_dto(updated_coach)
    
    async def get_all_coaches(self) -> List[CoachDTO]:
        """Get all coaches."""
        coaches = await self.coach_repository.list_all()
        return [self._to_dto(coach) for coach in coaches]
    
    async def get_coach_customers(self, coach_id: UUID) -> List[CustomerDTO]:
        """Get all customers assigned to a coach."""
        coach = await self.coach_repository.get_by_id(coach_id)
        if not coach:
            raise ValueError("Coach not found")
        
        customers = await self.customer_repository.get_by_coach_id(coach_id)
        return [self._customer_to_dto(customer) for customer in customers]
    
    async def assign_customer(self, dto: AssignCoachDTO, requesting_coach_id: UUID) -> CustomerDTO:
        """Assign a customer to a coach (coach can only assign to themselves)."""
        # Verify coach exists
        coach = await self.coach_repository.get_by_id(dto.coach_id)
        if not coach:
            raise ValueError("Coach not found")
        
        # Verify requesting coach matches the coach being assigned
        if requesting_coach_id != dto.coach_id:
            raise ValueError("Coaches can only assign customers to themselves")
        
        # Get customer
        customer = await self.customer_repository.get_by_id(dto.customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Assign coach
        customer.assign_coach(dto.coach_id)
        updated_customer = await self.customer_repository.update(customer)
        
        return self._customer_to_dto(updated_customer)
    
    def _to_dto(self, coach: Coach) -> CoachDTO:
        """Convert Coach entity to DTO."""
        from src.domain.entities.enums import UserType
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
    
    def _customer_to_dto(self, customer) -> CustomerDTO:
        """Convert Customer entity to DTO."""
        from src.domain.entities.enums import UserType
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
