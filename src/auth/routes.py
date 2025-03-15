from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, status, HTTPException, Depends
from src.users.schemas import UserBaseSchema, UserResponseSchema
from src.users.models import FactUser
from src.auth.utils import generate_passwd_hash
from src.users.service import UserService
from src.db.main import get_session

auth_router = APIRouter()
UserService = UserService()

@auth_router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data: UserBaseSchema, session: AsyncSession = Depends(get_session)):
    user_data_dict = user_data.model_dump()

    user_exists = await UserService.get_user_by_email(user_data_dict['email'], session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists you dickhead.")
    

    new_user = FactUser(
        **user_data_dict
    )

    new_user.password_hash = generate_passwd_hash(user_data_dict['password'])

    session.add(new_user)
    await session.commit()
    return new_user
