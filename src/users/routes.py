from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from src.db.models import User, Coaches, Students
from src.users.schemas import UserModel, CoachModel, StudentModel, UserCreateModel, CoachCreateModel, StudentCreateModel
from src.users.service import UserService, CoachService, StudentService
from src.db.main import get_session
from sqlmodel import select


user_router = APIRouter()

# Instantiate services
user_service = UserService()
coach_service = CoachService()
student_service = StudentService()

# Route to get all users
@user_router.get("/get_all_users", response_model=List[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    statement = select(User)
    result = await session.exec(statement)
    users = result.all()
    return users

# Route to get all coaches
@user_router.get("/get_all_coaches", response_model=List[CoachModel])
async def get_all_coaches(session: AsyncSession = Depends(get_session)):
    statement = select(Coaches)
    result = await session.exec(statement)
    coaches = result.all()
    return coaches

# Route to get all students
@user_router.get("/get_all_students", response_model=List[StudentModel])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    statement = select(Students)
    result = await session.exec(statement)
    students = result.all()
    return students

# Route to create a new user
@user_router.post("/create_user", response_model=UserModel)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    new_user = await user_service.create_a_user(user_data, session)
    if new_user.role == "Coach":
        coach_data = CoachCreateModel(**user_data.model_dump())
        await coach_service.create_coach(new_user.user_id, coach_data, session)
    if new_user.role == "Student":
        student_data = StudentCreateModel(**user_data.model_dump())
        await student_service.create_student(new_user.user_id, student_data, session)
    if new_user.role == "Both":
        student_data = StudentCreateModel(**user_data.model_dump())
        await student_service.create_student(new_user.user_id, student_data, session)

        coach_data = CoachCreateModel(**user_data.model_dump())
        await coach_service.create_coach(new_user.user_id, coach_data, session)

    return new_user