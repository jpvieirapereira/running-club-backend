from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from typing import List, Union
from uuid import UUID
from src.application.use_cases import TrainingPlanUseCase
from src.application.dtos import (
    CoachDTO, CustomerDTO,
    CreateTrainingPlanDTO, UpdateTrainingPlanDTO,
    CreateTrainingDayDTO, UpdateTrainingDayDTO
)
from src.presentation.schemas import (
    TrainingPlanCreate, TrainingPlanUpdate, TrainingPlanResponse,
    TrainingDayCreate, TrainingDayUpdate, TrainingDayResponse
)
from src.presentation.api.dependencies import get_current_active_user
from src.infrastructure.container import Container
from src.domain.entities.enums import UserType


router = APIRouter(prefix="/training-plans", tags=["Training Plans"])


@router.post("", response_model=TrainingPlanResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_training_plan(
    plan_data: TrainingPlanCreate,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    training_plan_use_case: TrainingPlanUseCase = Depends(Provide[Container.training_plan_use_case])
):
    """
    Create a new training plan.
    
    Only coaches can create training plans for their customers.
    """
    # Verify current user is a coach
    if current_user.user_type != UserType.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only coaches can create training plans"
        )
    
    try:
        # Convert training days
        training_days_dto = None
        if plan_data.training_days:
            training_days_dto = [
                CreateTrainingDayDTO(
                    date=day.date,
                    training_type=day.training_type,
                    zone=day.zone,
                    terrain=day.terrain,
                    distance_km=day.distance_km,
                    workout_details=day.workout_details,
                    day_order=day.day_order
                )
                for day in plan_data.training_days
            ]
        
        dto = CreateTrainingPlanDTO(
            customer_id=plan_data.customer_id,
            name=plan_data.name,
            start_date=plan_data.start_date,
            end_date=plan_data.end_date,
            description=plan_data.description,
            success_criteria=plan_data.success_criteria,
            training_days=training_days_dto
        )
        
        plan = await training_plan_use_case.create_plan(current_user.id, dto)
        
        return TrainingPlanResponse(
            id=plan.id,
            coach_id=plan.coach_id,
            customer_id=plan.customer_id,
            name=plan.name,
            start_date=plan.start_date,
            end_date=plan.end_date,
            description=plan.description,
            success_criteria=plan.success_criteria,
            is_active=plan.is_active,
            training_days=[
                TrainingDayResponse(
                    id=day.id,
                    training_plan_id=day.training_plan_id,
                    date=day.date,
                    training_type=day.training_type,
                    zone=day.zone,
                    terrain=day.terrain,
                    distance_km=day.distance_km,
                    workout_details=day.workout_details,
                    day_order=day.day_order
                )
                for day in plan.training_days
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{plan_id}", response_model=TrainingPlanResponse)
@inject
async def get_training_plan(
    plan_id: UUID,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    training_plan_use_case: TrainingPlanUseCase = Depends(Provide[Container.training_plan_use_case])
):
    """Get a training plan by ID."""
    try:
        plan = await training_plan_use_case.get_plan(plan_id)
        
        # Verify access: coach must own the plan or customer must be assigned to it
        if current_user.user_type == UserType.COACH:
            if plan.coach_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found")
        else:  # Customer
            if plan.customer_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found")
        
        return TrainingPlanResponse(
            id=plan.id,
            coach_id=plan.coach_id,
            customer_id=plan.customer_id,
            name=plan.name,
            start_date=plan.start_date,
            end_date=plan.end_date,
            description=plan.description,
            success_criteria=plan.success_criteria,
            is_active=plan.is_active,
            training_days=[
                TrainingDayResponse(
                    id=day.id,
                    training_plan_id=day.training_plan_id,
                    date=day.date,
                    training_type=day.training_type,
                    zone=day.zone,
                    terrain=day.terrain,
                    distance_km=day.distance_km,
                    workout_details=day.workout_details,
                    day_order=day.day_order
                )
                for day in plan.training_days
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=List[TrainingPlanResponse])
@inject
async def list_training_plans(
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    training_plan_use_case: TrainingPlanUseCase = Depends(Provide[Container.training_plan_use_case])
):
    """
    List training plans.
    
    - Coaches see all plans they created
    - Customers see all plans assigned to them
    """
    if current_user.user_type == UserType.COACH:
        plans = await training_plan_use_case.get_coach_plans(current_user.id)
    else:
        plans = await training_plan_use_case.get_customer_plans(current_user.id)
    
    return [
        TrainingPlanResponse(
            id=plan.id,
            coach_id=plan.coach_id,
            customer_id=plan.customer_id,
            name=plan.name,
            start_date=plan.start_date,
            end_date=plan.end_date,
            description=plan.description,
            success_criteria=plan.success_criteria,
            is_active=plan.is_active,
            training_days=[
                TrainingDayResponse(
                    id=day.id,
                    training_plan_id=day.training_plan_id,
                    date=day.date,
                    training_type=day.training_type,
                    zone=day.zone,
                    terrain=day.terrain,
                    distance_km=day.distance_km,
                    workout_details=day.workout_details,
                    day_order=day.day_order
                )
                for day in plan.training_days
            ]
        )
        for plan in plans
    ]


@router.put("/{plan_id}", response_model=TrainingPlanResponse)
@inject
async def update_training_plan(
    plan_id: UUID,
    plan_data: TrainingPlanUpdate,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    training_plan_use_case: TrainingPlanUseCase = Depends(Provide[Container.training_plan_use_case])
):
    """
    Update a training plan.
    
    Only coaches can update their own training plans.
    """
    if current_user.user_type != UserType.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only coaches can update training plans"
        )
    
    try:
        dto = UpdateTrainingPlanDTO(
            name=plan_data.name,
            start_date=plan_data.start_date,
            end_date=plan_data.end_date,
            description=plan_data.description,
            success_criteria=plan_data.success_criteria
        )
        
        plan = await training_plan_use_case.update_plan(plan_id, current_user.id, dto)
        
        return TrainingPlanResponse(
            id=plan.id,
            coach_id=plan.coach_id,
            customer_id=plan.customer_id,
            name=plan.name,
            start_date=plan.start_date,
            end_date=plan.end_date,
            description=plan.description,
            success_criteria=plan.success_criteria,
            is_active=plan.is_active,
            training_days=[
                TrainingDayResponse(
                    id=day.id,
                    training_plan_id=day.training_plan_id,
                    date=day.date,
                    training_type=day.training_type,
                    zone=day.zone,
                    terrain=day.terrain,
                    distance_km=day.distance_km,
                    workout_details=day.workout_details,
                    day_order=day.day_order
                )
                for day in plan.training_days
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_training_plan(
    plan_id: UUID,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    training_plan_use_case: TrainingPlanUseCase = Depends(Provide[Container.training_plan_use_case])
):
    """
    Delete a training plan.
    
    Only coaches can delete their own training plans.
    """
    if current_user.user_type != UserType.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only coaches can delete training plans"
        )
    
    try:
        await training_plan_use_case.delete_plan(plan_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{plan_id}/days", response_model=TrainingDayResponse, status_code=status.HTTP_201_CREATED)
@inject
async def add_training_day(
    plan_id: UUID,
    day_data: TrainingDayCreate,
    current_user: Union[CoachDTO, CustomerDTO] = Depends(get_current_active_user),
    training_plan_use_case: TrainingPlanUseCase = Depends(Provide[Container.training_plan_use_case])
):
    """
    Add a training day to a plan.
    
    Only coaches can add training days to their plans.
    """
    if current_user.user_type != UserType.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only coaches can add training days"
        )
    
    try:
        dto = CreateTrainingDayDTO(
            date=day_data.date,
            training_type=day_data.training_type,
            zone=day_data.zone,
            terrain=day_data.terrain,
            distance_km=day_data.distance_km,
            workout_details=day_data.workout_details,
            day_order=day_data.day_order
        )
        
        day = await training_plan_use_case.add_training_day(plan_id, current_user.id, dto)
        
        return TrainingDayResponse(
            id=day.id,
            training_plan_id=day.training_plan_id,
            date=day.date,
            training_type=day.training_type,
            zone=day.zone,
            terrain=day.terrain,
            distance_km=day.distance_km,
            workout_details=day.workout_details,
            day_order=day.day_order
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
