from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.api import deps
from app.models import ImagingStudy, User
from app.schemas.imaging import ImagingCreate, ImagingOut, ImagingUpdate
from app.services.audit import log_action
from app.services.dicom_connector import scan_and_import

router = APIRouter()


@router.get("", response_model=list[ImagingOut])
def list_imaging(db: Session = Depends(deps.get_db), patient_id: int | None = Query(None), study_date: date | None = Query(None)):
    query = db.query(ImagingStudy)
    if patient_id:
        query = query.filter(ImagingStudy.patient_id == patient_id)
    if study_date:
        query = query.filter(ImagingStudy.study_date == study_date)
    return query.all()


@router.get("/{study_id}", response_model=ImagingOut)
def get_imaging(study_id: int, db: Session = Depends(deps.get_db)):
    study = db.query(ImagingStudy).get(study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")
    return study


@router.post("/manual-link", response_model=ImagingOut)
def manual_link(imaging_in: ImagingCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    study = ImagingStudy(**imaging_in.dict())
    db.add(study)
    db.commit()
    db.refresh(study)
    log_action(db, "CREATE_IMAGING", "imaging_study", study.id, current_user.id, None)
    return study


@router.post("/import-once", response_model=list[ImagingOut])
def trigger_import(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    imported = scan_and_import(db)
    return imported
