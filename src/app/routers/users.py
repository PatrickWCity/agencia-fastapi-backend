from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.user import (
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)

router = APIRouter()


@router.post("/users/", response_model=UserPublic, tags=["users"])
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/", response_model=list[UserPublic], tags=["users"])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    users = session.exec(
        select(User).where(User.deleted_at is None).offset(offset).limit(limit)
    ).all()
    return users


@router.get("/users/{user_id}", response_model=UserPublic, tags=["users"])
def read_user(*, user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user | user.deleted_at is not None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserPublic, tags=["users"])
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user: UserUpdate,
):
    db_user = session.get(User, user_id)
    if not db_user | db_user.deleted_at is not None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now(timezone.utc)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", tags=["users"])
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user | user.deleted_at is not None:
        raise HTTPException(status_code=404, detail="User not found")
    user.deleted_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    return {"ok": True}
