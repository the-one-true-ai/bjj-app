from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from uuid import UUID
from src.db.models import User, Coaches, Students
from src.users.schemas import Input_forPublic_UserCreateSchema, Input_forSelf_CoachCreateModel, Input_forSelf_StudentCreateModel, Response_forSelf_CoachProfile, Response_forSelf_UserProfile, Response_forSelf_StudentProfile
from src.auth.utils import generate_passwd_hash
from fastapi import HTTPException


class UserService:
    def __init__(self):
        self.coach_service = CoachService()
        self.student_service = StudentService()

    async def _get_coachID_from_userID(self, user_id: UUID, session: AsyncSession):
        try:
            # Query the dim_students table to get the user_id by student_id
            statement = select(Coaches.coach_id).where(Coaches.user_id == user_id)
            result = await session.exec(statement)
            coach_id = result.first()  # Get the user_id or None if not found

            if not user_id:
                raise HTTPException(status_code=404, detail="Coach not found")  # Handle the case if no user found

            return coach_id  # Return the user_id directly

    async def _get_studentID_from_userID(self, user_id: UUID, session: AsyncSession):
        try:
            # Query the dim_students table to get the user_id by student_id
            statement = select(Students.student_id).where(Students.user_id == user_id)
            result = await session.exec(statement)
            student_id = result.first()  # Get the user_id or None if not found

            if not user_id:
                raise HTTPException(status_code=404, detail="Student not found")  # Handle the case if no user found

            return student_id  # Return the user_id directly

        except SQLAlchemyError as e:
            print(f"Database error trying to get user ID from student ID: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")  

    async def _get_userID_from_coachID(self, coach_id: UUID, session: AsyncSession):
        try:
            # Query the dim_students table to get the user_id by student_id
            statement = select(Coaches.user_id).where(Coaches.coach_id == coach_id)
            result = await session.exec(statement)
            user_id = result.first()  # Get the user_id or None if not found

            if not user_id:
                raise HTTPException(status_code=404, detail="Coach not found")  # Handle the case if no user found

            return user_id  # Return the user_id directly

        except SQLAlchemyError as e:
            print(f"Database error trying to get user ID from student ID: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")        

    async def _get_userID_from_studentID(self, student_id: UUID, session: AsyncSession):
        try:
            # Query the dim_students table to get the user_id by student_id
            statement = select(Students.user_id).where(Students.student_id == student_id)
            result = await session.exec(statement)
            user_id = result.first()  # Get the user_id or None if not found

            if not user_id:
                raise HTTPException(status_code=404, detail="Student not found")  # Handle the case if no user found

            return user_id  # Return the user_id directly

        except SQLAlchemyError as e:
            print(f"Database error trying to get user ID from student ID: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


    async def get_full_user_profile(self, user_id: UUID, session: AsyncSession):
        try:
            # Query user with related Coach and Student profiles
            statement = (
                select(User)
                .options(selectinload(User.coach))
                .options(selectinload(User.student))
                .where(User.user_id == user_id)
            )
            result = await session.exec(statement)
            user = result.first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Serialize user profile
            user_profile = Response_forSelf_UserProfile.model_validate(user)

            # Serialize coach profile if exists
            coach_profile = (
                Response_forSelf_CoachProfile.model_validate(user.coach) if user.coach else None
            )

            # Serialize student profile if exists
            student_profile = (
                Response_forSelf_StudentProfile.model_validate(user.student) if user.student else None
            )

            return {
                "user_profile": user_profile,
                "coach_profile": coach_profile,
                "student_profile": student_profile,
            }

        except SQLAlchemyError as e:
            print(f"Database error trying to get full user profile: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def _get_user_by_email(self, email: str, session: AsyncSession):
        try:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            user = result.first()
            return user
        except SQLAlchemyError as e:
            print(f"Database error trying to get user by email: {e}")
            return None    

    async def _get_user_by_id(self, user_id: UUID, session: AsyncSession):
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await session.exec(statement)
            user = result.first()
            return user
        except SQLAlchemyError as e:
            print(f"Database error trying to get user by id: {e}")
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

    async def create_a_user(self, user_data: Input_forPublic_UserCreateSchema, session: AsyncSession):
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


class CoachService:
    async def get_all_coaches(self, session: AsyncSession):
        try:
            statement = (
                select(Coaches, User)  # Select both Coaches and User models
                .join(User, User.user_id == Coaches.user_id)  # Join on user_id
            )
            result = await session.exec(statement)
            return result.all()  # Returns a list of all coaches
        except SQLAlchemyError as e:
            print(f"Database error trying to get all coaches: {e}")
            return []  # Return an empty list if there's an error

    async def get_coach_by_username(self, coach_username: str, session: AsyncSession):
        try:
            # Query to get the coach and its related user data
            statement = (
                select(Coaches, User)
                .join(User, User.user_id == Coaches.user_id)  # Ensure you join the related User model
                .where(Coaches.user.has(username=coach_username))
            )
            result = await session.exec(statement)
            coach = result.first()  # Get the first result
            
            if not coach:
                raise HTTPException(status_code=404, detail="Coach not found")
            
            # Map the coach and user data into the response model
            return coach  # This will be passed to the response model for serialization

        except SQLAlchemyError as e:
            print(f"Database error trying to get coach: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
            

    async def add_coach_record(self, user_id: UUID, coach_data: Input_forSelf_CoachCreateModel, session: AsyncSession):
        try:
            # Prepare coach data
            coach_data_dict = coach_data.model_dump()
            new_coach = Coaches(**coach_data_dict)
            new_coach.user_id = user_id  # Assign the user_id to the new coach

            # Ensure some columns in dim_user table are populated
            # ? Does this need to be done in this way?

            # Save coach to database
            session.add(new_coach)
            await session.commit()
            return new_coach  # Return the newly created coach

        except SQLAlchemyError as e:
            print(f"Database error trying to create a coach: {e}")
            return None



class StudentService:
    async def get_student_by_username(self, student_username: str, session: AsyncSession):
        try:
            statement = (
                select(Students)
                .join(Students.user)
                .where(Students.user.has(username=student_username)) # TODO: Add fuzzy lookup. Limit to Students only
            )
            result = await session.exec(statement)
            return result.all()
        except SQLAlchemyError as e:
            print(f"Database error trying to get student by username: {e}")
            return None

    
    async def create_student(self,user_id: UUID, student_data: Input_forSelf_StudentCreateModel, session: AsyncSession):
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
