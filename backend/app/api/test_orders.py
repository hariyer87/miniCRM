from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models import TestOrder, User
from app.schemas.test_order import TestOrderCreate, TestOrderOut, TestOrderUpdate
from app.services.audit import log_action

router = APIRouter()


@router.get("", response_model=list[TestOrderOut])
def list_orders(db: Session = Depends(deps.get_db), visit_id: int | None = Query(None), status: str | None = Query(None)):
    query = db.query(TestOrder)
    if visit_id:
        query = query.filter(TestOrder.visit_id == visit_id)
    if status:
        query = query.filter(TestOrder.status == status)
    return query.all()


@router.post("", response_model=TestOrderOut)
def create_order(order_in: TestOrderCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    order = TestOrder(**order_in.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    log_action(db, "CREATE_TEST_ORDER", "test_order", order.id, current_user.id, None)
    return order


@router.get("/{order_id}", response_model=TestOrderOut)
def get_order(order_id: int, db: Session = Depends(deps.get_db)):
    order = db.query(TestOrder).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=TestOrderOut)
def update_order(order_id: int, order_in: TestOrderUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    order = db.query(TestOrder).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in order_in.dict(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    log_action(db, "UPDATE_TEST_ORDER", "test_order", order.id, current_user.id, None)
    return order
