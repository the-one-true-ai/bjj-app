from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel, UserUpdateModel
from .models import User
from sqlmodel import select, desc
from datetime import datetime

class UserService:
    async def get_all_users(self, session:AsyncSession):
        statement = select(User).order_by(desc(User.uid))
        result = await session.exec(statement)

        return result.all()

    async def get_a_user(self, user_uid:str, session:AsyncSession):
        statement = select(User).where(User.uid == user_uid)
        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None

    async def create_a_user(self, user_data: UserCreateModel, session:AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )

        new_user.started_at = datetime.strptime(user_data_dict['started_at'], "%Y-%m-%d")

        session.add(new_user)
        await session.commit()
        
        return new_user

    async def update_a_user(self, user_uid: str, update_data: UserUpdateModel, session:AsyncSession):
        user_to_update = self.get_a_user(user_uid, session)
        if user_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                setattr(user_to_update, key, value)

            await session.commit()

            return user_to_update
        
        else:
            return None
        

    async def delete_a_user(self, user_uid:str, session:AsyncSession):
        user_to_delete = self.get_a_user(user_uid, session)
        if user_to_delete is not None:
            await session.delete(user_to_delete)
            await session.commit()
            return {}
        else:
            return None
