from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.users.schemas import UserBaseSchema, UserResponseSchema
from src.users.models import FactUser
from .utils import generate_passwd_hash, verify_passwd, create_access_token, decode_access_token
from src.users.service import UserService
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, TokenBearer
from src.db.main import get_session
from datetime import timedelta, datetime

auth_router = APIRouter()
UserService = UserService()
REFRESH_TOKEN_EXPIRY = 2 #days

@auth_router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data: UserBaseSchema, session: AsyncSession = Depends(get_session)):
    password = user_data.password
    user_data_dict = user_data.model_dump()

    user_exists = await UserService.get_user_by_email(user_data_dict['email'], session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists you dickhead.")
    

    new_user = FactUser(
        **user_data_dict
    )

    new_user.password_hash = generate_passwd_hash(password)

    session.add(new_user)
    await session.commit()
    return new_user

@auth_router.post("/login", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def login_user(user_login_data: UserBaseSchema, session: AsyncSession = Depends(get_session)):
    email = user_login_data.email
    password = user_login_data.password

    user_logging_in = await UserService.get_user_by_email(email, session)

    if not user_logging_in:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email does not exist.")

    else:
        if verify_passwd(password, user_logging_in.password_hash):
            access_token = create_access_token(
                user_data={
                    "email": user_logging_in.email,
                    "uid": str(user_logging_in.uid)},
                expires_delta=None)
        
            refresh_token = create_access_token(
                user_data={
                    "email": user_logging_in.email,
                    "uid": str(user_logging_in.uid)
                    },
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRY))
            
            return JSONResponse(
                content={
                    "message": "Login successful.",
                    "access_token": access_token, 
                    "refresh_token": refresh_token,
                    "user":{
                        "uid": str(user_logging_in.uid),
                        "email": user_logging_in.email
                        }
                    })      
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data={
                "user": token_details['user']})
        
        return JSONResponse(content={
            "access_token": new_access_token
            })
        

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")