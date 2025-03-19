from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID
from src.db.models import User, Coaches, Students
from src.users.schemas import UserModel, CoachModel, StudentModel, UserCreateModel, CoachCreateModel, StudentCreateModel
from src.auth.utils import generate_passwd_hash


class UserService:
    def __init__(self):
        self.coach_service = CoachService()
        self.student_service = StudentService()

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_a_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        # You no longer need to parse 'started_at' as it is already a datetime object
        new_user = User(
            **user_data_dict
        )
        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])

        # Remove the line that tries to parse started_at
        # new_user.started_at = datetime.strptime(user_data_dict['started_at'], "%Y-%m-%d")  # This is not needed.

        session.add(new_user)
        await session.commit()
        
        return new_user


class CoachService:
    async def get_coach_by_user_id(self, user_id: UUID, session: AsyncSession):
        statement = select(Coaches).where(Coaches.user_id == user_id)

        result = await session.exec(statement)

        coach = result.first()

        return coach

    async def create_coach(self, user_id: UUID, coach_data: CoachModel, session: AsyncSession):
        coach_data_dict = coach_data.model_dump()

        new_coach = Coaches(user_id=user_id, **coach_data_dict)

        session.add(new_coach)

        await session.commit()

        return new_coach

    async def update_coach(self, coach: Coaches, coach_data: dict, session: AsyncSession):
        for k, v in coach_data.items():
            setattr(coach, k, v)

        await session.commit()

        return coach


class StudentService:
    async def get_student_by_user_id(self, user_id: UUID, session: AsyncSession):
        statement = select(Students).where(Students.user_id == user_id)

        result = await session.exec(statement)

        student = result.first()

        return student

    async def create_student(self, user_id: UUID, student_data: StudentModel, session: AsyncSession):
        student_data_dict = student_data.model_dump()

        new_student = Students(user_id=user_id, **student_data_dict)

        session.add(new_student)

        await session.commit()

        return new_student

    async def update_student(self, student: Students, student_data: dict, session: AsyncSession):
        for k, v in student_data.items():
            setattr(student, k, v)

        await session.commit()

        return student
