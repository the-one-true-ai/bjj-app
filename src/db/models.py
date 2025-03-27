from datetime import datetime, date
from typing import List, Optional
from uuid import uuid4, UUID

from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Enum, String
from sqlmodel import Column, Field, Relationship, SQLModel

from src.users.validators import Role, Belt
from src.feedback.validators import MessageType, FeedbackStatus
from src.db.model_mixins import TimestampMixin, PIIMixin


class User(SQLModel, TimestampMixin, PIIMixin, table=True):
    __tablename__ = "dim_users"
    
    # Mandatory fields

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

    # Optional fields  
    height: Optional[int] = Field(
        default=None,
        sa_column=Column(pg.INTEGER, nullable=True)
    )
    weight: Optional[int] = Field(
        default=None,
        sa_column=Column(pg.INTEGER, nullable=True)
    )
    birthdate: Optional[date] = Field(default=None, sa_column=Column(pg.DATE, nullable=True))
    belt: Belt = Field(sa_column=Column(Enum(Belt), nullable=False))

    

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
    expertise: Optional[list[str]] = Field(sa_column=Column(ARRAY(String), nullable=True))
    affiliations: Optional[list[str]]  = Field(sa_column=Column(ARRAY(String), nullable=True))
    coach_bio: Optional[str]  # Bio specific to their coaching experience
    price: Optional[int] = Field(default=5, nullable=True)
    accepting_responses: bool = Field(default=True, nullable=False)

    # Relationship with User
    user: "User" = Relationship(back_populates="coach")  


class Students(SQLModel, TimestampMixin, table=True):
    __tablename__ = "dim_students"
    
    student_id: UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4))
    user_id: UUID = Field(foreign_key="dim_users.user_id")
    areas_working_on: Optional[list[str]] = Field(sa_column=Column(ARRAY(String), nullable=True))

    # Relationship with User
    user: "User" = Relationship(back_populates="student")  


class FeedbackSession(SQLModel, TimestampMixin, table=True):
    __tablename__ = "fact_feedbacksessions"

    feedback_session_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    student_id: UUID = Field(foreign_key="dim_students.student_id", nullable=False)
    coach_id: UUID = Field(foreign_key="dim_coaches.coach_id", nullable=False)
    title: str = Field(nullable=True)
    status: FeedbackStatus = Field(nullable=False)
    is_closed: bool = Field(default=False, nullable=False)
    closed_by_coach: bool = Field(default=False, nullable=False)
    closed_by_student: bool = Field(default=False, nullable=False)
    review_by_student: str = Field(nullable=True)
    review_by_coach: str = Field(nullable=True)
    date_closed: Optional[datetime] = Field(default=None, nullable=True)

    # One-to-many relationship with messages
    messages: List["Messages"] = Relationship(back_populates="feedback_session") 


class Messages(SQLModel, TimestampMixin, table=True):
    __tablename__ = "fact_messages"

    message_id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    feedback_session_id: UUID = Field(foreign_key="fact_feedbacksessions.feedback_session_id", nullable=False)
    sender_user_id: UUID = Field(foreign_key="dim_users.user_id", nullable=False)
    message_type: MessageType = Field(nullable=False)
    message_content: str = Field(nullable=False)  # Text or link to audio file

    # Back-populating the feedback session relationship
    feedback_session: FeedbackSession = Relationship(back_populates="messages")