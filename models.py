import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class Event(SQLModel, table=True):
    """Model representing an event in the system. """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)


class User(SQLModel, table=True):
    """User table model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    created_at: datetime = Field(default=datetime.datetime.now())
