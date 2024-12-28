from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, max_length=255)
    email: str = Field(index=True, max_length=255)
    full_name: str = Field(index=True, max_length=255)
    disabled: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int


class UserUpdate(SQLModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
