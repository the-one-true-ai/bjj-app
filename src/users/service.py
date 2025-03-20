from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from src.db.models import User, Coaches, Students
from src.users.schemas import UserCreateModel, CoachCreateModel, StudentCreateModel
from src.auth.utils import generate_passwd_hash
from fastapi import HTTPException


class UserService:
    def __init__(self):
        self.coach_service = CoachService()
        self.student_service = StudentService()

    async def get_all_users(self, session: AsyncSession):
        try:
            statement = select(User)
            result = await session.exec(statement)
            return result.all()
        except SQLAlchemyError as e:
            print(f"Database error trying to get all users: {e}")
            return []   
    
    async def get_user_by_id(self, user_id: UUID, session: AsyncSession):
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await session.exec(statement)
            user = result.first()
            return user
        except SQLAlchemyError as e:
            print(f"Database error trying to get user by id: {e}")
            return None
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        try:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            user = result.first()
            return user
        except SQLAlchemyError as e:
            print(f"Database error trying to get user by email: {e}")
            return None

    async def _username_exists(self, username: str, session: AsyncSession):
        try:
            statement = select(User).where(User.username == username)
            result = await session.exec(statement)
            user = result.first()
            return user is not None # Returns True if user exists, False otherwise
        except SQLAlchemyError as e:
            print(f"Database error trying to get user by username: {e}")
            return None

    async def create_a_user(self, user_data: UserCreateModel, session: AsyncSession):
        try:
            # Check if the username already exists
            if await self._username_exists(user_data.username, session):
                raise HTTPException(status_code=400, detail="Username already exists.")

            # Prepare user data
            user_data_dict = user_data.model_dump()
            new_user = User(**user_data_dict)
            new_user.password_hash = generate_passwd_hash(user_data_dict["password"])

            # Save user to database
            session.add(new_user)
            await session.commit()
            return new_user  # Return the newly created user

        except SQLAlchemyError as e:
            print(f"Database error trying to create a user: {e}")
            # Raise HTTPException with a 500 status code for any database error
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update_user_by_id(self, user_id: UUID, user_data: dict, session: AsyncSession):
        # Need to add logic to add/delete rows from dim_student and dim_coach if the role changes.
        try:
            # Use get_user_by_id to fetch the user
            user = await self.get_user_by_id(user_id, session)
            user_data = user_data.model_dump()

            if not user:
                return None  # Return None if the user doesn't exist

            # Only update fields that are not None
            for key, value in user_data.items():
                if value is not None:
                    setattr(user, key, value)

            # Commit changes to the database
            await session.commit()
            return user  # Return the updated user

        except SQLAlchemyError as e:
            print(f"Database error trying to update user: {e}")
            return None

        
    async def delete_user_by_id():
        pass


class CoachService:
    async def get_all_coaches(self, session: AsyncSession):
        try:
            statement = select(Coaches)
            result = await session.exec(statement)
            return result.all()  # Returns a list of all coaches
        except SQLAlchemyError as e:
            print(f"Database error trying to get all coaches: {e}")
            return []  # Return an empty list if there's an error

    async def get_coach_by_user_id(self, user_id: UUID, session: AsyncSession):
        try:
            statement = select(Coaches).where(Coaches.user_id == user_id)
            result = await session.exec(statement)
            return result.first()
        except SQLAlchemyError as e:
            print(f"Database error trying to get coach by user id: {e}")
            return None

    async def get_coach_by_coach_id(self, coach_id: UUID, session: AsyncSession):
        try:
            statement = select(Coaches).where(Coaches.coach_id == coach_id)
            result = await session.exec(statement)
            return result.first()
        except SQLAlchemyError as e:
            print(f"Database error trying to get coach by coach id: {e}")
            return None

    async def get_coach_by_expertise():
        pass

    async def create_coach(self, user_id: UUID, coach_data: CoachCreateModel, session: AsyncSession):
        try:
            # Prepare coach data
            coach_data_dict = coach_data.model_dump()
            new_coach = Coaches(**coach_data_dict)
            new_coach.user_id = user_id  # Assign the user_id to the new coach

            # Save coach to database
            session.add(new_coach)
            await session.commit()
            return new_coach  # Return the newly created coach

        except SQLAlchemyError as e:
            print(f"Database error trying to create a coach: {e}")
            return None



class StudentService:
    async def get_all_students(self, session: AsyncSession):
        try:
            statement = select(Students)
            result = await session.exec(statement)
            return result.all()  # Returns a list of all students
        except SQLAlchemyError as e:
            print(f"Database error trying to get all students: {e}")
            return []  # Return an empty list if there's an error
    
    async def get_student_by_user_id(self, user_id: UUID, session: AsyncSession):
        try:
            statement = select(Students).where(Students.user_id == user_id)
            result = await session.exec(statement)
            return result.first()
        except SQLAlchemyError as e:
            print(f"Database error trying to get student by user id: {e}")
            return None

    async def get_student_by_student_id(self, student_id: UUID, session: AsyncSession):
        try:
            statement = select(Students).where(Students.student_id == student_id)
            result = await session.exec(statement)
            return result.first()
        except SQLAlchemyError as e:
            print(f"Database error trying to get student by student id: {e}")
            return None
    
    async def create_student(self,user_id: UUID, student_data: StudentCreateModel, session: AsyncSession):
        try:
            # Prepare student data
            student_data_dict = student_data.model_dump()
            new_student = Students(**student_data_dict)
            new_student.user_id = user_id

            # Save student to database
            session.add(new_student)
            await session.commit()
            return new_student  # Return the newly created student

        except SQLAlchemyError as e:
            print(f"Database error trying to create a student: {e}")
            return None
