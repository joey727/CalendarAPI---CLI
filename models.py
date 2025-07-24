import datetime
from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional


class Recurrence(str, Enum):
    """To handle recurring events"""
    none = "none"
    daily = "daily"
    weekly = "weekly"


class Event(SQLModel, table=True):
    """Model representing an event in the system. """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    recurrence: Recurrence = Recurrence.none


class User(SQLModel, table=True):
    """User table model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
