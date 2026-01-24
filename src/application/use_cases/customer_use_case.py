from typing import List
from uuid import UUID
from src.domain.entities.customer import Customer
from src.domain.repositories.customer_repository import CustomerRepository
from src.infrastructure.auth.auth_service import AuthService
from src.application.dtos import CustomerDTO, CreateCustomerDTO, UpdateCustomerDTO
from src.domain.entities.enums import UserType


class CustomerUseCase:
    """Use case for customer operations."""
    
    def __init__(
        self,
        customer_repository: CustomerRepository,
        auth_service: AuthService
    ):
        self.customer_repository = customer_repository
        self.auth_service = auth_service
    
    async def register(self, dto: CreateCustomerDTO) -> CustomerDTO:
        """Register a new customer."""
        # Check if email already exists
        existing_customer = await self.customer_repository.get_by_email(dto.email)
        if existing_customer:
            raise ValueError("User with this email already exists")
        
        # Check if CPF already exists
        existing_by_doc = await self.customer_repository.get_by_document_number(dto.document_number)
        if existing_by_doc:
            raise ValueError("CPF already registered")
        
        # Create new customer
        hashed_password = self.auth_service.get_password_hash(dto.password)
        customer = Customer(
            email=dto.email,
            hashed_password=hashed_password,
            name=dto.name,
            phone=dto.phone,
            date_of_birth=dto.date_of_birth,
            document_number=dto.document_number,
            runner_level=dto.runner_level,
            training_availability=dto.training_availability,
            challenge_next_month=dto.challenge_next_month,
            nickname=dto.nickname
        )
        
        created_customer = await self.customer_repository.create(customer)
        
        return self._to_dto(created_customer)
    
    async def update_profile(self, customer_id: UUID, dto: UpdateCustomerDTO) -> CustomerDTO:
        """Update customer profile."""
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Update only provided fields
        if dto.name is not None:
            customer.name = dto.name
        if dto.phone is not None:
            customer.phone = dto.phone
        if dto.nickname is not None:
            customer.nickname = dto.nickname
        if dto.runner_level is not None:
            customer.runner_level = dto.runner_level
        if dto.training_availability is not None:
            customer.training_availability = dto.training_availability
        if dto.challenge_next_month is not None:
            customer.challenge_next_month = dto.challenge_next_month
        
        updated_customer = await self.customer_repository.update(customer)
        
        return self._to_dto(updated_customer)
    
    async def get_all_customers(self) -> List[CustomerDTO]:
        """Get all customers."""
        customers = await self.customer_repository.list_all()
        return [self._to_dto(customer) for customer in customers]
    
    def _to_dto(self, customer: Customer) -> CustomerDTO:
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
