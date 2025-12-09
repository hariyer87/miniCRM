from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BillingBase(BaseModel):
    visit_id: int
    subtotal_amount: Optional[float] = 0
    discount_amount: Optional[float] = 0
    total_amount: Optional[float] = 0
    amount_paid: Optional[float] = 0
    balance_amount: Optional[float] = 0
    payment_mode: Optional[str] = None
    status: Optional[str] = "unpaid"


class BillingCreate(BillingBase):
    pass


class BillingUpdate(BaseModel):
    subtotal_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    total_amount: Optional[float] = None
    amount_paid: Optional[float] = None
    balance_amount: Optional[float] = None
    payment_mode: Optional[str] = None
    status: Optional[str] = None


class BillingOut(BillingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
