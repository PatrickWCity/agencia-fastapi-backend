from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.power import (
    Power,
    PowerCreate,
    PowerPublic,
    PowerPublicWithHero,
    PowerUpdate,
)

router = APIRouter()


@router.post("/powers/", response_model=PowerPublic, tags=["powers"])
def create_power(*, session: Session = Depends(get_session), power: PowerCreate):
    db_power = Power.model_validate(power)
    session.add(db_power)
    session.commit()
    session.refresh(db_power)
    return db_power


@router.get("/powers/", response_model=list[PowerPublic], tags=["powers"])
def read_powers(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    powers = session.exec(
        select(Power).where(Power.deleted_at == None).offset(offset).limit(limit)
    ).all()
    return powers


@router.get(
    "/powers/{power_id}",
    response_model=PowerPublicWithHero,
    tags=["powers"],
)
def read_power(*, session: Session = Depends(get_session), power_id: int):
    power = session.get(Power, power_id)
    if not power or power.deleted_at != None:
        raise HTTPException(status_code=404, detail="Power not found")
    return power


@router.patch("/powers/{power_id}", response_model=PowerPublic, tags=["powers"])
def update_power(
    *, session: Session = Depends(get_session), power_id: int, power: PowerUpdate
):
    db_power = session.get(Power, power_id)
    if not db_power or db_power.deleted_at != None:
        raise HTTPException(status_code=404, detail="Power not found")
    power_data = power.model_dump(exclude_unset=True)
    for key, value in power_data.items():
        setattr(db_power, key, value)
    db_power.updated_at = datetime.now(timezone.utc)
    session.add(db_power)
    session.commit()
    session.refresh(db_power)
    return db_power


@router.delete("/powers/{power_id}", tags=["powers"])
def delete_power(*, session: Session = Depends(get_session), power_id: int):
    power = session.get(Power, power_id)
    if not power or power.deleted_at != None:
        raise HTTPException(status_code=404, detail="Power not found")
    power.deleted_at = datetime.now(timezone.utc)
    if power.hero:
        power.hero_id = None
        power.updated_at = datetime.now(timezone.utc)
    session.add(power)
    session.commit()
    return {"ok": True}
