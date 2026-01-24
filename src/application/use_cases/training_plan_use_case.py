from typing import List
from uuid import UUID
from src.domain.entities.training_plan import TrainingPlan
from src.domain.entities.training_day import TrainingDay
from src.domain.repositories.training_plan_repository import TrainingPlanRepository
from src.domain.repositories.customer_repository import CustomerRepository
from src.application.dtos import (
    TrainingPlanDTO, CreateTrainingPlanDTO, UpdateTrainingPlanDTO,
    TrainingDayDTO, CreateTrainingDayDTO, UpdateTrainingDayDTO
)


class TrainingPlanUseCase:
    """Use case for training plan operations."""
    
    def __init__(
        self,
        training_plan_repository: TrainingPlanRepository,
        customer_repository: CustomerRepository
    ):
        self.training_plan_repository = training_plan_repository
        self.customer_repository = customer_repository
    
    async def create_plan(self, coach_id: UUID, dto: CreateTrainingPlanDTO) -> TrainingPlanDTO:
        """Create a new training plan."""
        # Verify customer exists and belongs to coach
        customer = await self.customer_repository.get_by_id(dto.customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        if customer.coach_id != coach_id:
            raise ValueError("Customer is not assigned to this coach")
        
        # Create plan
        plan = TrainingPlan(
            coach_id=coach_id,
            customer_id=dto.customer_id,
            name=dto.name,
            start_date=dto.start_date,
            end_date=dto.end_date,
            description=dto.description,
            success_criteria=dto.success_criteria
        )
        
        created_plan = await self.training_plan_repository.create(plan)
        
        # Add training days if provided
        training_days = []
        if dto.training_days:
            for day_dto in dto.training_days:
                training_day = TrainingDay(
                    training_plan_id=created_plan.id,
                    date=day_dto.date,
                    training_type=day_dto.training_type,
                    zone=day_dto.zone,
                    terrain=day_dto.terrain,
                    distance_km=day_dto.distance_km,
                    workout_details=day_dto.workout_details,
                    day_order=day_dto.day_order
                )
                created_day = await self.training_plan_repository.add_training_day(training_day)
                training_days.append(self._training_day_to_dto(created_day))
        
        return self._to_dto(created_plan, training_days)
    
    async def get_plan(self, plan_id: UUID) -> TrainingPlanDTO:
        """Get training plan by ID."""
        plan = await self.training_plan_repository.get_by_id(plan_id)
        if not plan:
            raise ValueError("Training plan not found")
        
        training_days = await self.training_plan_repository.get_training_days(plan_id)
        training_day_dtos = [self._training_day_to_dto(day) for day in training_days]
        
        return self._to_dto(plan, training_day_dtos)
    
    async def update_plan(self, plan_id: UUID, coach_id: UUID, dto: UpdateTrainingPlanDTO) -> TrainingPlanDTO:
        """Update training plan."""
        plan = await self.training_plan_repository.get_by_id(plan_id)
        if not plan:
            raise ValueError("Training plan not found")
        
        # Verify ownership
        if plan.coach_id != coach_id:
            raise ValueError("You can only update your own training plans")
        
        # Update plan
        plan.update_info(
            name=dto.name,
            description=dto.description,
            success_criteria=dto.success_criteria,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        
        updated_plan = await self.training_plan_repository.update(plan)
        training_days = await self.training_plan_repository.get_training_days(plan_id)
        training_day_dtos = [self._training_day_to_dto(day) for day in training_days]
        
        return self._to_dto(updated_plan, training_day_dtos)
    
    async def delete_plan(self, plan_id: UUID, coach_id: UUID) -> bool:
        """Delete training plan."""
        plan = await self.training_plan_repository.get_by_id(plan_id)
        if not plan:
            raise ValueError("Training plan not found")
        
        # Verify ownership
        if plan.coach_id != coach_id:
            raise ValueError("You can only delete your own training plans")
        
        return await self.training_plan_repository.delete(plan_id)
    
    async def get_coach_plans(self, coach_id: UUID) -> List[TrainingPlanDTO]:
        """Get all plans created by a coach."""
        plans = await self.training_plan_repository.get_by_coach_id(coach_id)
        result = []
        for plan in plans:
            training_days = await self.training_plan_repository.get_training_days(plan.id)
            training_day_dtos = [self._training_day_to_dto(day) for day in training_days]
            result.append(self._to_dto(plan, training_day_dtos))
        return result
    
    async def get_customer_plans(self, customer_id: UUID) -> List[TrainingPlanDTO]:
        """Get all plans assigned to a customer."""
        plans = await self.training_plan_repository.get_by_customer_id(customer_id)
        result = []
        for plan in plans:
            training_days = await self.training_plan_repository.get_training_days(plan.id)
            training_day_dtos = [self._training_day_to_dto(day) for day in training_days]
            result.append(self._to_dto(plan, training_day_dtos))
        return result
    
    async def add_training_day(
        self,
        plan_id: UUID,
        coach_id: UUID,
        dto: CreateTrainingDayDTO
    ) -> TrainingDayDTO:
        """Add a training day to a plan."""
        plan = await self.training_plan_repository.get_by_id(plan_id)
        if not plan:
            raise ValueError("Training plan not found")
        
        # Verify ownership
        if plan.coach_id != coach_id:
            raise ValueError("You can only modify your own training plans")
        
        training_day = TrainingDay(
            training_plan_id=plan_id,
            date=dto.date,
            training_type=dto.training_type,
            zone=dto.zone,
            terrain=dto.terrain,
            distance_km=dto.distance_km,
            workout_details=dto.workout_details,
            day_order=dto.day_order
        )
        
        created_day = await self.training_plan_repository.add_training_day(training_day)
        return self._training_day_to_dto(created_day)
    
    async def update_training_day(
        self,
        training_day_id: UUID,
        coach_id: UUID,
        dto: UpdateTrainingDayDTO
    ) -> TrainingDayDTO:
        """Update a training day."""
        # Get the training day's plan to verify ownership
        training_days = await self.training_plan_repository.get_training_days(training_day_id)
        # Implementation note: This needs refinement - should get day by ID first
        
        # For now, simplified version
        raise NotImplementedError("Update training day needs plan lookup")
    
    async def delete_training_day(
        self,
        training_day_id: UUID,
        coach_id: UUID
    ) -> bool:
        """Delete a training day."""
        # Verify ownership through plan
        # Implementation note: Needs plan lookup
        return await self.training_plan_repository.delete_training_day(training_day_id)
    
    def _to_dto(self, plan: TrainingPlan, training_days: List[TrainingDayDTO]) -> TrainingPlanDTO:
        """Convert TrainingPlan entity to DTO."""
        return TrainingPlanDTO(
            id=plan.id,
            coach_id=plan.coach_id,
            customer_id=plan.customer_id,
            name=plan.name,
            start_date=plan.start_date,
            end_date=plan.end_date,
            description=plan.description,
            success_criteria=plan.success_criteria,
            is_active=plan.is_active,
            training_days=training_days
        )
    
    def _training_day_to_dto(self, day: TrainingDay) -> TrainingDayDTO:
        """Convert TrainingDay entity to DTO."""
        return TrainingDayDTO(
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
