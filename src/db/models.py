import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel, Relationship


from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

class User(SQLModel, table=True):
    __tablename__ = "dim_users"
    
    user_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    username: str
    role: str = "Student"
    email: str
    password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False), exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # Define relationships
    coach: "Coaches" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    student: "Students" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})


class Coaches(SQLModel, table=True):
    __tablename__ = "dim_coaches"
    
    coach_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    user_id: UUID = Field(foreign_key="dim_users.user_id")  # Foreign key to User table
    expertise: Optional[str]  # E.g., 'Leglocks, Escapes, Takedowns'
    affiliations: Optional[str]  # E.g., Gym name
    coach_bio: Optional[str]  # Bio specific to their coaching experience

    # Relationship with User
    user: "User" = Relationship(back_populates="coach")


class Students(SQLModel, table=True):
    __tablename__ = "dim_students"
    
    student_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    user_id: UUID = Field(foreign_key="dim_users.user_id")  # Foreign key to User table
    areas_working_on: Optional[str]  # E.g., 'Guard Passing, Sweeps'

    # Relationship with User
    user: "User" = Relationship(back_populates="student")
