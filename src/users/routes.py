from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from src.db.models import User, Coaches, Students
from src.users.schemas import Input_forPublic_UserCreateSchema, Input_forSelf_CoachCreateModel, Input_forSelf_StudentCreateModel, Response_forSelf_UserSchema, Response_forPublic_CoachProfile, Response_forAccountHolder_CoachProfile
from src.users.service import UserService, CoachService, StudentService
from src.db.main import get_session
from sqlmodel import select
from src.auth.dependencies import RoleChecker, AccessTokenBearer, RefreshTokenBearer, get_current_user


user_router = APIRouter()

# Instantiate services
user_service = UserService()
coach_service = CoachService()
student_service = StudentService()


# Routes for Users

# Route to create a user
@user_router.post("/create_user", response_model=Response_forSelf_UserSchema)
async def create_user(user_data: Input_forPublic_UserCreateSchema, session: AsyncSession = Depends(get_session)) -> Response_forSelf_UserSchema:
    new_user = await user_service.create_a_user(user_data, session)
    if new_user.role == "Coach":
        coach_data = Input_forSelf_CoachCreateModel(**user_data.model_dump())
        print("Raw user_data:", user_data.model_dump())
        await coach_service.add_coach_record(new_user.user_id, coach_data, session)
    
    if new_user.role == "Student":
        student_data = Input_forSelf_StudentCreateModel(**user_data.model_dump())
        await student_service.create_student(new_user.user_id, student_data, session)
    
    if new_user.role == "Both":
        student_data = Input_forSelf_StudentCreateModel(**user_data.model_dump())
        await student_service.create_student(new_user.user_id, student_data, session)

        coach_data = Input_forSelf_CoachCreateModel(**user_data.model_dump())
        print(user_data)
        await coach_service.add_coach_record(new_user.user_id, coach_data, session)

    return new_user

@user_router.get("/my_profile") # TODO: This should be a new Response_forSelf_ProfileSchema
async def my_profile(user = Depends(get_current_user), session: AsyncSession = Depends(get_session), token_data: dict = Depends(AccessTokenBearer())):# -> Response_forSelf_UserSchema: # TODO: This should be a new Response_forSelf_ProfileSchema
    result = await user_service.get_full_user_profile(user_id=user.user_id,session=session)
    return result

# Routes for Coaches


# Route to get all coaches
@user_router.get("/public/get_all_coaches", response_model=List[Response_forPublic_CoachProfile])
async def get_all_coaches(session: AsyncSession = Depends(get_session)) -> List[Response_forPublic_CoachProfile]:
    result = await coach_service.get_all_coaches(session)
    return [
        Response_forPublic_CoachProfile(
            **coach.model_dump(),  # Dynamically extract all fields from the Coach object
            username=user.username,  # Include the username from the User object
            affiliation=coach.affiliations if coach.affiliations else None  # Handle optional affiliation
        )
        for coach, user in result  # Unpack each tuple into coach and user
    ]

@user_router.get("/authorised/get_all_coaches", response_model=List[Response_forAccountHolder_CoachProfile])
async def get_all_coaches(session: AsyncSession = Depends(get_session), token_data: dict = Depends(AccessTokenBearer())) -> List[Response_forAccountHolder_CoachProfile]:
    result = await coach_service.get_all_coaches(session)
    return [
        Response_forAccountHolder_CoachProfile(
            **coach.model_dump(),  # Dynamically extract all fields from the Coach object
            username=user.username,  # Include the username from the User object
            affiliation=coach.affiliations if coach.affiliations else None  # Handle optional affiliation
        )
        for coach, user in result  # Unpack each tuple into coach and user
    ]

@user_router.get("/authorised/coach/{coach_username}", response_model=Response_forAccountHolder_CoachProfile)
async def get_coach_by_username(
        coach_username: str,
        session: AsyncSession = Depends(get_session),
        token_data: dict = Depends(AccessTokenBearer()) # To make sure only logged-in users can access this.
        ) -> Response_forAccountHolder_CoachProfile:

    coach, user = await coach_service.get_coach_by_username(coach_username=coach_username, session=session)
    return Response_forAccountHolder_CoachProfile(
        **coach.model_dump(),  # This will include coach fields
        username=user.username  # Add the user field
    )



@user_router.get("/public/coach/{coach_username}", response_model=Response_forPublic_CoachProfile)
async def get_coach_by_username(
        coach_username: str,
        session: AsyncSession = Depends(get_session)) -> Response_forPublic_CoachProfile:

    coach, user = await coach_service.get_coach_by_username(coach_username=coach_username, session=session)
    return Response_forPublic_CoachProfile(
        **coach.model_dump(),  # This will include coach fields
        username=user.username  # Add the user field
    )

