from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=["bcrypt"]
    )

def generate_passwd_hash(readable_password_string: str) -> str:
    return passwd_context.hash(readable_password_string)

def verify_passwd(readable_password_string: str, hashed_password: str) -> bool:
    return passwd_context.verify(readable_password_string, hashed_password)