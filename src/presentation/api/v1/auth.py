from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from typing import Union, List
from uuid import UUID
from src.application.use_cases import AuthenticationUseCase, CoachUseCase, CustomerUseCase
from src.application.dtos import (
    CreateCoachDTO, CreateCustomerDTO, CoachDTO, CustomerDTO,
    UpdateCoachDTO, UpdateCustomerDTO, LoginDTO, AssignCoachDTO
)
from src.presentation.schemas import (
    CoachCreate, CoachUpdate, CoachResponse,
    CustomerCreate, CustomerUpdate, CustomerResponse,
    Token, LoginRequest, AssignCoach
)
from src.presentation.api.dependencies import get_current_active_user
from src.infrastructure.container import Container
from src.domain.entities.enums import UserType


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/coach", response_model=CoachResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register_coach(
    coach_data: CoachCreate,
    coach_use_case: CoachUseCase = Depends(Provide[Container.coach_use_case])
):
    """Register a new coach."""
    try:
        dto = CreateCoachDTO(
            email=coach_data.email,
            password=coach_data.password,
            name=coach_data.name,
            phone=coach_data.phone,
            date_of_birth=coach_data.date_of_birth,
            document_number=coach_data.document_number,
            bio=coach_data.bio,
            specialization=coach_data.specialization,
            nickname=coach_data.nickname
        )
        coach = await coach_use_case.register(dto)
        return CoachResponse(
            id=coach.id,
            email=coach.email,
            name=coach.name,
            phone=coach.phone,
            date_of_birth=coach.date_of_birth,
            document_number=coach.document_number,
            user_type=coach.user_type,
            nickname=coach.nickname,
            bio=coach.bio,
            specialization=coach.specialization,
            is_active=coach.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/register/customer", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register_customer(
    customer_data: CustomerCreate,
    customer_use_case: CustomerUseCase = Depends(Provide[Container.customer_use_case])
):
    """Register a new customer."""
    try:
        dto = CreateCustomerDTO(
            email=customer_data.email,
            password=customer_data.password,
            name=customer_data.name,
            phone=customer_data.phone,
            date_of_birth=customer_data.date_of_birth,
            document_number=customer_data.document_number,
            runner_level=customer_data.runner_level,
            training_availability=customer_data.training_availability,
            challenge_next_month=customer_data.challenge_next_month,
            nickname=customer_data.nickname
        )
        customer = await customer_use_case.register(dto)
        return CustomerResponse(
            id=customer.id,
            email=customer.email,
            name=customer.name,
            phone=customer.phone,
            date_of_birth=customer.date_of_birth,
            document_number=customer.document_number,
            user_type=customer.user_type,
            nickname=customer.nickname,
            runner_level=customer.runner_level,
            training_availability=customer.training_availability,
            challenge_next_month=customer.challenge_next_month,
            coach_id=customer.coach_id,
            is_active=customer.is_active
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


@router.get("/me", response_model=Union[CoachResponse, CustomerResponse])
async def get_me(current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user)):
    """Get current user information."""
    if current_user.user_type == UserType.COACH:
        return CoachResponse(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            phone=current_user.phone,
            date_of_birth=current_user.date_of_birth,
            document_number=current_user.document_number,
            user_type=current_user.user_type,
            nickname=current_user.nickname,
            bio=current_user.bio,
            specialization=current_user.specialization,
            is_active=current_user.is_active
        )
    else:
        return CustomerResponse(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            phone=current_user.phone,
            date_of_birth=current_user.date_of_birth,
            document_number=current_user.document_number,
            user_type=current_user.user_type,
            nickname=current_user.nickname,
            runner_level=current_user.runner_level,
            training_availability=current_user.training_availability,
            challenge_next_month=current_user.challenge_next_month,
            coach_id=current_user.coach_id,
            is_active=current_user.is_active
        )


@router.put("/me", response_model=Union[CoachResponse, CustomerResponse])
@inject
async def update_profile(
    update_data: Union[CoachUpdate, CustomerUpdate],
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    coach_use_case: CoachUseCase = Depends(Provide[Container.coach_use_case]),
    customer_use_case: CustomerUseCase = Depends(Provide[Container.customer_use_case])
):
    """
    Update current user profile.
    
    The request body should match the user type (coach or customer).
    """
    try:
        if current_user.user_type == UserType.COACH:
            if not isinstance(update_data, CoachUpdate):
                update_data = CoachUpdate(**update_data.model_dump(exclude_unset=True))
            dto = UpdateCoachDTO(
                name=update_data.name,
                phone=update_data.phone,
                nickname=update_data.nickname,
                bio=update_data.bio,
                specialization=update_data.specialization
            )
            updated_user = await coach_use_case.update_profile(current_user.id, dto)
            return CoachResponse(
                id=updated_user.id,
                email=updated_user.email,
                name=updated_user.name,
                phone=updated_user.phone,
                date_of_birth=updated_user.date_of_birth,
                document_number=updated_user.document_number,
                user_type=updated_user.user_type,
                nickname=updated_user.nickname,
                bio=updated_user.bio,
                specialization=updated_user.specialization,
                is_active=updated_user.is_active
            )
        else:
            if not isinstance(update_data, CustomerUpdate):
                update_data = CustomerUpdate(**update_data.model_dump(exclude_unset=True))
            dto = UpdateCustomerDTO(
                name=update_data.name,
                phone=update_data.phone,
                nickname=update_data.nickname,
                runner_level=update_data.runner_level,
                training_availability=update_data.training_availability,
                challenge_next_month=update_data.challenge_next_month
            )
            updated_user = await customer_use_case.update_profile(current_user.id, dto)
            return CustomerResponse(
                id=updated_user.id,
                email=updated_user.email,
                name=updated_user.name,
                phone=updated_user.phone,
                date_of_birth=updated_user.date_of_birth,
                document_number=updated_user.document_number,
                user_type=updated_user.user_type,
                nickname=updated_user.nickname,
                runner_level=updated_user.runner_level,
                training_availability=updated_user.training_availability,
                challenge_next_month=updated_user.challenge_next_month,
                coach_id=updated_user.coach_id,
                is_active=updated_user.is_active
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/coaches", response_model=List[CoachResponse])
@inject
async def list_coaches(
    coach_use_case: CoachUseCase = Depends(Provide[Container.coach_use_case])
):
    """List all coaches."""
    coaches = await coach_use_case.get_all_coaches()
    return [
        CoachResponse(
            id=coach.id,
            email=coach.email,
            name=coach.name,
            phone=coach.phone,
            date_of_birth=coach.date_of_birth,
            document_number=coach.document_number,
            user_type=coach.user_type,
            nickname=coach.nickname,
            bio=coach.bio,
            specialization=coach.specialization,
            is_active=coach.is_active
        )
        for coach in coaches
    ]


@router.get("/coaches/{coach_id}/customers", response_model=List[CustomerResponse])
@inject
async def get_coach_customers(
    coach_id: UUID,
    coach_use_case: CoachUseCase = Depends(Provide[Container.coach_use_case])
):
    """Get all customers assigned to a specific coach."""
    try:
        customers = await coach_use_case.get_coach_customers(coach_id)
        return [
            CustomerResponse(
                id=customer.id,
                email=customer.email,
                name=customer.name,
                phone=customer.phone,
                date_of_birth=customer.date_of_birth,
                document_number=customer.document_number,
                user_type=customer.user_type,
                nickname=customer.nickname,
                runner_level=customer.runner_level,
                training_availability=customer.training_availability,
                challenge_next_month=customer.challenge_next_month,
                coach_id=customer.coach_id,
                is_active=customer.is_active
            )
            for customer in customers
        ]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/customers/assign-coach", response_model=CustomerResponse)
@inject
async def assign_coach_to_customer(
    assign_data: AssignCoach,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    coach_use_case: CoachUseCase = Depends(Provide[Container.coach_use_case])
):
    """
    Assign a customer to the current coach.
    
    Only coaches can assign customers to themselves.
    """
    try:
        # Verify current user is a coach
        if current_user.user_type != UserType.COACH:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only coaches can assign customers"
            )
        
        dto = AssignCoachDTO(
            customer_id=assign_data.customer_id,
            coach_id=current_user.id
        )
        updated_customer = await coach_use_case.assign_customer(dto, current_user.id)
        return CustomerResponse(
            id=updated_customer.id,
            email=updated_customer.email,
            name=updated_customer.name,
            phone=updated_customer.phone,
            date_of_birth=updated_customer.date_of_birth,
            document_number=updated_customer.document_number,
            user_type=updated_customer.user_type,
            nickname=updated_customer.nickname,
            runner_level=updated_customer.runner_level,
            training_availability=updated_customer.training_availability,
            challenge_next_month=updated_customer.challenge_next_month,
            coach_id=updated_customer.coach_id,
            is_active=updated_customer.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

