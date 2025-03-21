from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from src.db.models import User, Coaches, Students
from src.users.schemas import UserModel, CoachModel, StudentModel, UserCreateModel, CoachCreateModel, StudentCreateModel, UserUpdateModel
from src.users.service import UserService, CoachService, StudentService
from src.db.main import get_session
from sqlmodel import select
from src.auth.dependencies import RoleChecker


user_router = APIRouter()

# Instantiate services
user_service = UserService()
coach_service = CoachService()
student_service = StudentService()

#
# Routes for Users
#

# Route to get all users
@user_router.get("/get_all_users", response_model=List[UserModel])
async def get_all_users(
        session: AsyncSession = Depends(get_session),
        role_access: bool = Depends(RoleChecker(["Admin"])) # Only admins can access this endpoint.
        ) -> List[UserModel]:
    result = await user_service.get_all_users(session)
    return result

# Route to get user by id
@user_router.get("/get_user_by_id/{user_id}", response_model=UserModel)
async def get_user_by_id(user_id: UUID, session: AsyncSession = Depends(get_session)) -> UserModel:
    result = await user_service.get_user_by_id(user_id, session)
    return result

# Route to get user by email
@user_router.get("/get_user_by_email/{email}", response_model=UserModel)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)) -> UserModel:
    result = await user_service.get_user_by_email(email, session)
    return result

# Route to create a user
@user_router.post("/create_user", response_model=UserModel)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)) -> UserModel:
    new_user = await user_service.create_a_user(user_data, session)
    print(new_user.role)
    print(new_user)
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

# Route to update a user
@user_router.patch("/update_user/{user_id}", response_model=UserModel)
async def update_user(user_id: UUID, user_data: UserUpdateModel, session: AsyncSession = Depends(get_session)) -> UserModel:
    updated_user = await user_service.update_user_by_id(user_id, user_data, session)
    return updated_user


# Route to delete a user
@user_router.delete("/delete_user/{user_id}", response_model=UserModel)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    deleted_user = await user_service.delete_user(user_id, session)
    return deleted_user


#
# Routes for Coaches
#


# Route to get all coaches
@user_router.get("/get_all_coaches", response_model=List[CoachModel])
async def get_all_coaches(session: AsyncSession = Depends(get_session)) -> List[CoachModel]:
    result = await coach_service.get_all_coaches(session)
    return result


# Route to get coach by user id
@user_router.get("/get_coach_by_user_id/{user_id}", response_model=CoachModel)
async def get_coach_by_user_id(user_id: UUID, session: AsyncSession = Depends(get_session)) -> CoachModel:
    result = await coach_service.get_coach_by_user_id(user_id, session)
    return result

# Route to get coach by coach id
@user_router.get("/get_coach_by_coach_id/{coach_id}", response_model=CoachModel)
async def get_coach_by_coach_id(coach_id: UUID, session: AsyncSession = Depends(get_session)) -> CoachModel:
    result = await coach_service.get_coach_by_coach_id(coach_id, session)
    return result


# Route to create a coach
@user_router.post("/create_coach/{user_id}", response_model=CoachModel)
async def create_coach(user_id: UUID, coach_data: CoachCreateModel, session: AsyncSession = Depends(get_session)) -> CoachModel:

    if await coach_service.get_coach_by_user_id(user_id, session):
        new_coach = await coach_service.create_coach(user_id, coach_data, session)
    else:
        print('UserID does not exist.')
        return None



#
# Routes for Students
#


# Route to get all students
@user_router.get("/get_all_students", response_model=List[CoachModel])
async def get_all_students(session: AsyncSession = Depends(get_session)) -> List[StudentModel]:
    result = await student_service.get_all_students(session)
    return result


# Route to get student by user id
@user_router.get("/get_student_by_user_id/{user_id}", response_model=StudentModel)
async def get_student_by_user_id(user_id: UUID, session: AsyncSession = Depends(get_session)) -> StudentModel:
    result = await student_service.get_student_by_user_id(user_id, session)
    return result

# Route to get student by coach id
@user_router.get("/get_student_by_student_id/{student_id}", response_model=StudentModel)
async def get_coach_by_coach_id(student_id: UUID, session: AsyncSession = Depends(get_session)) -> StudentModel:
    result = await student_service.get_student_by_student_id(student_id, session)
    return result


# Route to create a student
@user_router.post("/create_student/{user_id}", response_model=StudentModel)
async def create_coach(user_id: UUID, student_data: StudentCreateModel, session: AsyncSession = Depends(get_session)) -> StudentModel:

    if await student_service.get_student_by_user_id(user_id, session):
        new_coach = await student_service.create_coach(user_id, student_data, session)
    else:
        print('UserID does not exist.')
        return None












# Route to get all students
@user_router.get("/get_all_students", response_model=List[StudentModel])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    statement = select(Students)
    result = await session.exec(statement)
    students = result.all()
    return students
