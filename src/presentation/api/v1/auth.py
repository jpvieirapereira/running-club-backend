from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from src.application.use_cases import AuthenticationUseCase
from src.application.dtos import CreateUserDTO, LoginDTO, UserDTO
from src.presentation.schemas import UserCreate, UserResponse, Token, LoginRequest
from src.presentation.api.dependencies import get_current_active_user
from src.infrastructure.container import Container


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_data: UserCreate,
    auth_use_case: AuthenticationUseCase = Depends(Provide[Container.authentication_use_case])
):
    """Register a new user."""
    try:
        dto = CreateUserDTO(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        user = await auth_use_case.register(dto)
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthenticationUseCase = Depends(Provide[Container.authentication_use_case])
):
    """Login with OAuth2 password flow."""
    try:
        dto = LoginDTO(email=form_data.username, password=form_data.password)
        token = await auth_use_case.login(dto)
        return Token(access_token=token.access_token, token_type=token.token_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/login-json", response_model=Token)
@inject
async def login_json(
    login_data: LoginRequest,
    auth_use_case: AuthenticationUseCase = Depends(Provide[Container.authentication_use_case])
):
    """Login with JSON body (alternative to form data)."""
    try:
        dto = LoginDTO(email=login_data.email, password=login_data.password)
        token = await auth_use_case.login(dto)
        return Token(access_token=token.access_token, token_type=token.token_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserDTO = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active
    )
