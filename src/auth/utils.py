from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging 

passwd_context = CryptContext(
    schemes=["bcrypt"]
    )

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(readable_password_string: str) -> str:
    return passwd_context.hash(readable_password_string)

def verify_passwd(readable_password_string: str, hashed_password: str) -> bool:
    return passwd_context.verify(readable_password_string, hashed_password)

def create_access_token(user_data: dict, expires_delta: timedelta = None, refresh: bool = False) -> str:
    payload = {}    
    payload['user'] = user_data
    payload['exp'] = datetime.now() + expires_delta if expires_delta is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY) # If expiry not given it defaults to 1hr (3600 seconds)
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
        )
    
    return token
    

def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
            )
        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(f"Error decoding token: {e}")
        return None