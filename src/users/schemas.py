from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

class UserUpdateModel(User):
    name: str