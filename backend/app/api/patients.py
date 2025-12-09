from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models import Patient, User
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate
from app.services.audit import log_action

router = APIRouter()


@router.get("", response_model=list[PatientOut])
def list_patients(
    db: Session = Depends(deps.get_db),
    search: str | None = Query(None),
    patient_code: str | None = Query(None),
):
    query = db.query(Patient).filter(Patient.is_active == True)
    if search:
        query = query.filter((Patient.first_name.ilike(f"%{search}%")) | (Patient.last_name.ilike(f"%{search}%")) | (Patient.phone.ilike(f"%{search}%")))
    if patient_code:
        query = query.filter(Patient.patient_code == patient_code)
    return query.all()


@router.post("", response_model=PatientOut)
def create_patient(patient_in: PatientCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    patient = Patient(**patient_in.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    log_action(db, "CREATE_PATIENT", "patient", patient.id, current_user.id, None)
    return patient


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(deps.get_db)):
    patient = db.query(Patient).get(patient_id)
    if not patient or not patient.is_active:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, patient_in: PatientUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for field, value in patient_in.dict(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    log_action(db, "UPDATE_PATIENT", "patient", patient.id, current_user.id, None)
    return patient


@router.patch("/{patient_id}/deactivate", response_model=PatientOut)
def deactivate_patient(patient_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient.is_active = False
    db.commit()
    db.refresh(patient)
    log_action(db, "DEACTIVATE_PATIENT", "patient", patient.id, current_user.id, None)
    return patient
