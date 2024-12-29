from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.weapon import (
    Weapon,
    WeaponCreate,
    WeaponPublic,
    WeaponPublicWithHeroes,
    WeaponUpdate,
)

router = APIRouter()


@router.post("/weapons/", response_model=WeaponPublic, tags=["weapons"])
def create_weapon(*, session: Session = Depends(get_session), weapon: WeaponCreate):
    db_weapon = Weapon.model_validate(weapon)
    session.add(db_weapon)
    session.commit()
    session.refresh(db_weapon)
    return db_weapon


@router.get("/weapons/", response_model=list[WeaponPublic], tags=["weapons"])
def read_weapons(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    weapons = session.exec(
        select(Weapon).where(Weapon.deleted_at == None).offset(offset).limit(limit)
    ).all()
    return weapons


@router.get(
    "/weapons/{weapon_id}", response_model=WeaponPublicWithHeroes, tags=["weapons"]
)
def read_weapon(*, weapon_id: int, session: Session = Depends(get_session)):
    weapon = session.get(Weapon, weapon_id)
    if not weapon or weapon.deleted_at != None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon


@router.patch("/weapons/{weapon_id}", response_model=WeaponPublic, tags=["weapons"])
def update_weapon(
    *,
    session: Session = Depends(get_session),
    weapon_id: int,
    weapon: WeaponUpdate,
):
    db_weapon = session.get(Weapon, weapon_id)
    if not db_weapon or db_weapon.deleted_at != None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    weapon_data = weapon.model_dump(exclude_unset=True)
    for key, value in weapon_data.items():
        setattr(db_weapon, key, value)
    db_weapon.updated_at = datetime.now(timezone.utc)
    session.add(db_weapon)
    session.commit()
    session.refresh(db_weapon)
    return db_weapon


@router.delete("/weapons/{weapon_id}", tags=["weapons"])
def delete_weapon(*, session: Session = Depends(get_session), weapon_id: int):
    weapon = session.get(Weapon, weapon_id)
    if not weapon or weapon.deleted_at != None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    weapon.deleted_at = datetime.now(timezone.utc)
    for db_hero in weapon.heroes:
        db_hero.updated_at = datetime.now(timezone.utc)
        session.add(db_hero)
    weapon.heroes.clear()
    session.add(weapon)
    session.commit()
    return {"ok": True}
