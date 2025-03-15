from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserUpdateSchema
from .models import FactUser
from sqlmodel import select, desc
from datetime import datetime


class UserService:
    async def get_all_users(self, session: AsyncSession):
        statement = select(FactUser).order_by(desc(FactUser.uid))
        result = await session.exec(statement)
        return result.all()

    async def get_user_by_id(self, user_uid: str, session: AsyncSession):
        statement = select(FactUser).where(FactUser.uid == user_uid)
        result = await session.exec(statement)
        user = result.first()

        return user if user is not None else None
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(FactUser).where(FactUser.email == email)
        result = await session.exec(statement)
        user = result.first()

        return user if user is not None else None

    async def update_a_user(self, user_uid: str, update_data: UserUpdateSchema, session: AsyncSession):
        user_to_update = await self.get_user_by_id(user_uid, session)
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
