from typing import Optional
from uuid import UUID
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.auth.auth_service import AuthService
from src.application.dtos import UserDTO, CreateUserDTO, LoginDTO, TokenDTO


class AuthenticationUseCase:
    """Use case for user authentication."""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    async def register(self, dto: CreateUserDTO) -> UserDTO:
        """Register a new user."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        hashed_password = self.auth_service.get_password_hash(dto.password)
        user = User(
            email=dto.email,
            hashed_password=hashed_password,
            name=dto.name,
            document_number=dto.document_number,
            date_of_birth=dto.date_of_birth,
            phone=dto.phone,
            nickname=dto.nickname,
            runner_level=dto.runner_level,
            training_availability=dto.training_availability,
            challenge_next_month=dto.challenge_next_month
        )
        
        created_user = await self.user_repository.create(user)
        
        return UserDTO(
            id=created_user.id,
            email=created_user.email,
            name=created_user.name,
            document_number=created_user.document_number,
            date_of_birth=created_user.date_of_birth,
            phone=created_user.phone,
            nickname=created_user.nickname,
            runner_level=created_user.runner_level,
            training_availability=created_user.training_availability,
            challenge_next_month=created_user.challenge_next_month,
            is_active=created_user.is_active
        )
    
    async def login(self, dto: LoginDTO) -> TokenDTO:
        """Authenticate user and return token."""
        user = await self.user_repository.get_by_email(dto.email)
        
        if not user or not self.auth_service.verify_password(dto.password, user.hashed_password):
            raise ValueError("Incorrect email or password")
        
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        access_token = self.auth_service.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return TokenDTO(access_token=access_token)
    
    async def get_current_user(self, token: str) -> Optional[UserDTO]:
        """Get current user from token."""
        payload = self.auth_service.decode_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await self.user_repository.get_by_id(UUID(user_id))
        if not user:
            return None
        
        return UserDTO(
            id=user.id,
            email=user.email,
            name=user.name,
            document_number=user.document_number,
            date_of_birth=user.date_of_birth,
            phone=user.phone,
            nickname=user.nickname,
            runner_level=user.runner_level,
            training_availability=user.training_availability,
            challenge_next_month=user.challenge_next_month,
            is_active=user.is_active
        )
