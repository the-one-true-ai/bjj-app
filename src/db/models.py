from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Enum, String
from sqlmodel import Column, Field, Relationship, SQLModel

from src.users.validators import Role
from src.db.model_mixins import TimestampMixin, PIIMixin

class User(SQLModel, TimestampMixin, PIIMixin, table=True):
    __tablename__ = "dim_users"
    
    user_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    username: str
    role: str = Column(Enum(Role), nullable=False)  # Use Enum directly
    email: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, info={"is_pii": True})
    )  # Mark as PII
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )

    # Define relationships
    coach: Optional["Coaches"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    student: Optional["Students"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )


class Coaches(SQLModel, TimestampMixin, table=True):
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


class Students(SQLModel, TimestampMixin, table=True):
    __tablename__ = "dim_students"
    
    student_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    user_id: UUID = Field(foreign_key="dim_users.user_id")  # Foreign key to User table
    areas_working_on: Optional[str]  # E.g., 'Guard Passing, Sweeps'

    # Relationship with User
    user: "User" = Relationship(back_populates="student")