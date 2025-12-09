from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api import deps
from app.models import BillingRecord, Visit, User
from app.schemas.billing import BillingCreate, BillingOut, BillingUpdate
from app.services.audit import log_action

router = APIRouter()


@router.get("/visits/{visit_id}", response_model=BillingOut)
def get_billing(visit_id: int, db: Session = Depends(deps.get_db)):
    record = db.query(BillingRecord).filter(BillingRecord.visit_id == visit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Billing not found")
    return record


@router.post("/visits/{visit_id}", response_model=BillingOut)
def upsert_billing(visit_id: int, billing_in: BillingCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    record = db.query(BillingRecord).filter(BillingRecord.visit_id == visit_id).first()
    if not record:
        record = BillingRecord(**billing_in.dict())
        db.add(record)
        action = "CREATE_BILLING"
    else:
        for field, value in billing_in.dict(exclude_unset=True).items():
            setattr(record, field, value)
        action = "UPDATE_BILLING"
    db.commit()
    db.refresh(record)
    log_action(db, action, "billing_record", record.id, current_user.id, None)
    return record


@router.get("/summary", response_model=dict)
def billing_summary(summary_date: date = Query(..., description="YYYY-MM-DD"), db: Session = Depends(deps.get_db)):
    total_revenue = db.query(func.sum(BillingRecord.total_amount)).filter(func.date(BillingRecord.created_at) == summary_date).scalar() or 0
    total_paid = db.query(func.sum(BillingRecord.amount_paid)).filter(func.date(BillingRecord.created_at) == summary_date).scalar() or 0
    total_balance = db.query(func.sum(BillingRecord.balance_amount)).filter(func.date(BillingRecord.created_at) == summary_date).scalar() or 0
    return {
        "date": summary_date,
        "total_revenue": float(total_revenue),
        "total_paid": float(total_paid),
        "total_balance": float(total_balance),
    }
