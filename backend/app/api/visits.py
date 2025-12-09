from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models import Visit, User
from app.schemas.visit import VisitCreate, VisitOut, VisitUpdate
from app.services.audit import log_action

router = APIRouter()


@router.get("", response_model=list[VisitOut])
def list_visits(
    db: Session = Depends(deps.get_db),
    patient_id: int | None = Query(None),
    status: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
):
    query = db.query(Visit)
    if patient_id:
        query = query.filter(Visit.patient_id == patient_id)
    if status:
        query = query.filter(Visit.status == status)
    if start_date:
        query = query.filter(Visit.visit_date >= start_date)
    if end_date:
        query = query.filter(Visit.visit_date <= end_date)
    return query.all()


@router.post("", response_model=VisitOut)
def create_visit(visit_in: VisitCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    visit = Visit(**visit_in.dict())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    log_action(db, "CREATE_VISIT", "visit", visit.id, current_user.id, None)
    return visit


@router.get("/{visit_id}", response_model=VisitOut)
def get_visit(visit_id: int, db: Session = Depends(deps.get_db)):
    visit = db.query(Visit).get(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.put("/{visit_id}", response_model=VisitOut)
def update_visit(visit_id: int, visit_in: VisitUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    visit = db.query(Visit).get(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    for field, value in visit_in.dict(exclude_unset=True).items():
        setattr(visit, field, value)
    db.commit()
    db.refresh(visit)
    log_action(db, "UPDATE_VISIT", "visit", visit.id, current_user.id, None)
    return visit
