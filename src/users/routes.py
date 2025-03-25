from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from src.db.models import User, Coaches, Students
from src.users.schemas import UserModel, CoachModel, StudentModel, UserCreateModel, Input_forSelf_CoachCreateModel, StudentCreateModel, UserUpdateModel
from src.users.service import UserService, CoachService, StudentService
from src.db.main import get_session
from sqlmodel import select
from src.auth.dependencies import RoleChecker, AccessTokenBearer, RefreshTokenBearer


user_router = APIRouter()

# Instantiate services
user_service = UserService()
coach_service = CoachService()
student_service = StudentService()


# Routes for Users

# Route to create a user
@user_router.post("/create_user", response_model=UserModel)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)) -> UserModel:
    new_user = await user_service.create_a_user(user_data, session)
    print(new_user.role)
    print(new_user)
    if new_user.role == "Coach":
        coach_data = Input_forSelf_CoachCreateModel(**user_data.model_dump())
        await coach_service.add_coach_record(new_user.user_id, coach_data, session)
    
    if new_user.role == "Student":
        student_data = StudentCreateModel(**user_data.model_dump())
        await student_service.create_student(new_user.user_id, student_data, session)
    
    if new_user.role == "Both":
        student_data = StudentCreateModel(**user_data.model_dump())
        await student_service.create_student(new_user.user_id, student_data, session)

        coach_data = Input_forSelf_CoachCreateModel(**user_data.model_dump())
        await coach_service.add_coach_record(new_user.user_id, coach_data, session)

    return new_user


# Routes for Coaches


# Route to get all coaches
@user_router.get("/get_all_coaches", response_model=List[CoachModel])
async def get_all_coaches(session: AsyncSession = Depends(get_session)) -> List[CoachModel]:
    result = await coach_service.get_all_coaches(session)
    return result


@user_router.get("/authorised/coach/{coach_username}", response_model=CoachModel) #TODO: Make this a Response_forAccountHolder_CoachProfile
async def get_coach_by_username(
        coach_username: str,
        session: AsyncSession = Depends(get_session),
        token_data: dict = Depends(AccessTokenBearer()) # To make sure only logged-in users can access this.
        ):
    # This is to allow account holders to see more details about the coach. This can include a longer bio, more showcase videos, social media links, competition history etc.
    # This should only be done via a click-through from the Coach's chat channels with the student to prevent coaches from just browsing students and any PII issues.
    result = await coach_service.get_coach_by_username(coach_username=coach_username, session=session)
    return result

@user_router.get("/public/coach/{coach_username}", response_model=CoachModel) #TODO: Make this a Response_forPublic_CoachProfile
async def get_coach_by_username(
        coach_username: str,
        session: AsyncSession = Depends(get_session)):
    # This is to allow account holders to see more details about the coach. This can include a longer bio, more showcase videos, social media links, competition history etc.
    # This should only be done via a click-through from the Coach's chat channels with the student to prevent coaches from just browsing students and any PII issues.
    result = await coach_service.get_coach_by_username(coach_username=coach_username, session=session)
    return result


# Routes for Students

