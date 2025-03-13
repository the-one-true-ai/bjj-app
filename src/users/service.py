from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserBaseSchema, UserUpdateSchema
from .models import FactUser, FactCoach, FactStudent
from sqlmodel import select, desc
from datetime import datetime

class UserService:
    async def get_all_users(self, session: AsyncSession):
        statement = select(FactUser).order_by(desc(FactUser.uid))
        result = await session.exec(statement)
        return result.all()

    async def get_a_user(self, user_uid: str, session: AsyncSession):
        statement = select(FactUser).where(FactUser.uid == user_uid)
        result = await session.exec(statement)
        user = result.first()

        return user if user is not None else None

    async def create_a_user(self, user_data: UserBaseSchema, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        # You no longer need to parse 'started_at' as it is already a datetime object
        new_user = FactUser(
            **user_data_dict
        )

        # Remove the line that tries to parse started_at
        # new_user.started_at = datetime.strptime(user_data_dict['started_at'], "%Y-%m-%d")  # This is not needed.

        session.add(new_user)
        await session.commit()
        
        # Optionally create a student or coach record (if applicable)
        if user_data.role == "coach":
            new_coach = FactCoach(uid=new_user.uid)
            session.add(new_coach)
            await session.commit()
        
        if user_data.role == "student":
            new_student = FactStudent(uid=new_user.uid)
            session.add(new_student)
            await session.commit()

        if user_data.role == "both":
            new_student = FactStudent(uid=new_user.uid)
            new_coach = FactCoach(uid=new_user.uid)
            session.add(new_student)
            session.add(new_coach)
            await session.commit()


        return new_user

    async def update_a_user(self, user_uid: str, update_data: UserUpdateSchema, session: AsyncSession):
        user_to_update = await self.get_a_user(user_uid, session)
        if user_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                if value is not None:
                    setattr(user_to_update, key, value)

            # Ensure updated_at is always updated
            user_to_update.updated_at = datetime.now()

            await session.commit()
            return user_to_update
        else:
            return None

    async def delete_a_user(self, user_uid: str, session: AsyncSession):
        user_to_delete = await self.get_a_user(user_uid, session)
        if user_to_delete is not None:
            await session.delete(user_to_delete)
            await session.commit()
            return {}
        else:
            return None