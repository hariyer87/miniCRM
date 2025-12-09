from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import TestResult, TestOrder, User
from app.schemas.test_result import TestResultCreate, TestResultOut, TestResultUpdate
from app.services.audit import log_action

router = APIRouter()


@router.get("/{test_order_id}", response_model=TestResultOut)
def get_result(test_order_id: int, db: Session = Depends(deps.get_db)):
    result = db.query(TestResult).filter(TestResult.test_order_id == test_order_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.post("", response_model=TestResultOut)
def create_result(result_in: TestResultCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    if db.query(TestResult).filter(TestResult.test_order_id == result_in.test_order_id).first():
        raise HTTPException(status_code=400, detail="Result already exists")
    result = TestResult(**result_in.dict())
    db.add(result)
    db.commit()
    db.refresh(result)
    log_action(db, "CREATE_RESULT", "test_result", result.id, current_user.id, None)
    return result


@router.put("/{result_id}", response_model=TestResultOut)
def update_result(result_id: int, result_in: TestResultUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    result = db.query(TestResult).get(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    for field, value in result_in.dict(exclude_unset=True).items():
        setattr(result, field, value)
    db.commit()
    db.refresh(result)
    log_action(db, "UPDATE_RESULT", "test_result", result.id, current_user.id, None)
    return result


@router.post("/{result_id}/finalize", response_model=TestResultOut)
def finalize_result(result_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    result = db.query(TestResult).get(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    result.status = "final"
    result.finalized_at = datetime.utcnow()
    result.finalized_by_user_id = current_user.id
    db.commit()
    db.refresh(result)
    log_action(db, "FINALIZE_RESULT", "test_result", result.id, current_user.id, None)
    return result
