"""
Admin Use Case.
"""
from typing import List
from uuid import UUID

from src.domain.repositories import AdminRepository
from src.domain.entities.admin import Admin
from src.application.dtos import AdminDTO, CreateAdminDTO
from src.infrastructure.auth import AuthService


class AdminUseCase:
    """Use case for admin operations."""
    
    def __init__(
        self,
        admin_repository: AdminRepository,
        auth_service: AuthService
    ):
        """
        Initialize use case.
        
        Args:
            admin_repository: Admin repository
            auth_service: Authentication service
        """
        self.admin_repository = admin_repository
        self.auth_service = auth_service
    
    async def create_admin(self, data: CreateAdminDTO) -> AdminDTO:
        """
        Create a new admin user.
        
        Args:
            data: Admin creation data
        
        Returns:
            Created admin DTO
        
        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        existing = await self.admin_repository.get_by_email(data.email)
        if existing:
            raise ValueError(f"Admin with email {data.email} already exists")
        
        # Hash password
        hashed_password = self.auth_service.hash_password(data.password)
        
        # Create admin entity
        admin = Admin(
            email=data.email,
            hashed_password=hashed_password,
            name=data.name,
            phone=data.phone,
            date_of_birth=data.date_of_birth,
            nickname=data.nickname
        )
        
        # Save to repository
        created = await self.admin_repository.create(admin)
        
        return self._to_dto(created)
    
    async def get_admin_by_id(self, admin_id: UUID) -> AdminDTO:
        """
        Get admin by ID.
        
        Args:
            admin_id: Admin ID
        
        Returns:
            Admin DTO
        
        Raises:
            ValueError: If admin not found
        """
        admin = await self.admin_repository.get_by_id(admin_id)
        if not admin:
            raise ValueError("Admin not found")
        
        return self._to_dto(admin)
    
    async def get_all_admins(self) -> List[AdminDTO]:
        """
        Get all admins.
        
        Returns:
            List of admin DTOs
        """
        admins = await self.admin_repository.get_all()
        return [self._to_dto(admin) for admin in admins]
    
    def _to_dto(self, admin: Admin) -> AdminDTO:
        """Convert admin entity to DTO."""
        return AdminDTO(
            id=admin.id,
            email=admin.email,
            name=admin.name,
            phone=admin.phone,
            date_of_birth=admin.date_of_birth,
            user_type=admin.user_type,
            nickname=admin.nickname,
            is_active=admin.is_active
        )
