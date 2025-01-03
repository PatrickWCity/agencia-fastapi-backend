from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.tag import (
    Tag,
    TagCreate,
    TagPublic,
    TagPublicWithItems,
    TagUpdate,
)

router = APIRouter()


@router.post("/tags/", response_model=TagPublic, tags=["tags"])
def create_tag(*, session: Session = Depends(get_session), tag: TagCreate):
    db_tag = Tag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


@router.get("/tags/", response_model=list[TagPublic], tags=["tags"])
def read_tags(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    tags = session.exec(
        select(Tag).where(Tag.deleted_at == None).offset(offset).limit(limit)
    ).all()
    return tags


@router.get("/tags/{tag_id}", response_model=TagPublicWithItems, tags=["tags"])
def read_tag(*, tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag or tag.deleted_at != None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/tags/{tag_id}", response_model=TagPublic, tags=["tags"])
def update_tag(
    *,
    session: Session = Depends(get_session),
    tag_id: int,
    tag: TagUpdate,
):
    db_tag = session.get(Tag, tag_id)
    if not db_tag or db_tag.deleted_at != None:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_data = tag.model_dump(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(db_tag, key, value)
    db_tag.updated_at = datetime.now(timezone.utc)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


@router.delete("/tags/{tag_id}", tags=["tags"])
def delete_tag(*, session: Session = Depends(get_session), tag_id: int):
    tag = session.get(Tag, tag_id)
    if not tag or tag.deleted_at != None:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag.deleted_at = datetime.now(timezone.utc)
    for db_item in tag.items:
        db_item.updated_at = datetime.now(timezone.utc)
        session.add(db_item)
    tag.items.clear()
    session.add(tag)
    session.commit()
    return {"ok": True}
