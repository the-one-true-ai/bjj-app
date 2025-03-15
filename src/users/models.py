import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String

# FactUser (Base Table)
class FactUser(SQLModel, table=True):
    __tablename__ = "dim_user_test"

    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    email: str = Field(default="unknown@example.com", sa_column=Column(String, nullable=False))  # Default placeholder email
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  