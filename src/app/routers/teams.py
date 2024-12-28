from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.team import (
    Team,
    TeamCreate,
    TeamPublic,
    TeamPublicWithHeroes,
    TeamUpdate,
)

router = APIRouter()


@router.post("/teams/", response_model=TeamPublic, tags=["teams"])
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/teams/", response_model=list[TeamPublic], tags=["teams"])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    teams = session.exec(
        select(Team).where(Team.deleted_at is None).offset(offset).limit(limit)
    ).all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamPublicWithHeroes, tags=["teams"])
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team | team.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/teams/{team_id}", response_model=TeamPublic, tags=["teams"])
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team | db_team.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    db_team.updated_at = datetime.now(timezone.utc)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/teams/{team_id}", tags=["teams"])
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team | team.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Team not found")
    team.deleted_at = datetime.now(timezone.utc)
    session.add(team)
    session.commit()
    return {"ok": True}
