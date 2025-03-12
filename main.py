from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Relationship, SQLModel, create_engine, Session, Field, Column, Integer, String, select


class Gym(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    members: list["User"] = Relationship(back_populates="gym")


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    gym_id: Optional[int] = Field(default=None, foreign_key="gym.id")
    gym: Optional[Gym] = Relationship(back_populates="users")


# FastAPI app
app = FastAPI()

# Database
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SQLModel.metadata.create_all(engine)

# Deps
def get_session():
    with Session(engine) as session:
        yield session


# Create a User
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Get all users
@app.get("/users/", response_model=list[User])
def get_all_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

# Get user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"There is no user with ID: {user_id}")
    return user
    
# Update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"There is no user with ID: {user_id}")

    user_data_dict = user_data.model_dump(exclude_unset=True)  # Only update provided fields
    for field, value in user_data_dict.items():
        setattr(user, field, value)   

    session.commit()
    session.refresh(user)
    return user


# Delete a user
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"There is no user with ID: {user_id}")

    session.delete(user)
    session.commit()
    return user    