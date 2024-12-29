from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(
        index=True, max_length=255, description="The username of the user"
    )
    email: EmailStr = Field(
        index=True, max_length=255, description="The email of the user"
    )
    full_name: str = Field(
        index=True, max_length=255, description="The full name of the user"
    )
    disabled: bool
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The timestamp when the user was created",
    )
    updated_at: Optional[datetime] = Field(
        description="The timestamp when the user was updated"
    )
    deleted_at: Optional[datetime] = Field(
        description="The timestamp when the user was deleted"
    )


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
