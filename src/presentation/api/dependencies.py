from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from src.application.use_cases import AuthenticationUseCase
from src.application.dtos import UserDTO
from src.infrastructure.container import Container


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_use_case: AuthenticationUseCase = Depends(Provide[Container.authentication_use_case])
) -> UserDTO:
    """Dependency to get current authenticated user."""
    user = await auth_use_case.get_current_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: UserDTO = Depends(get_current_user)
) -> UserDTO:
    """Dependency to get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
