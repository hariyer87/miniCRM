from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VisitBase(BaseModel):
    patient_id: int
    visit_date: Optional[datetime] = None
    referring_doctor: Optional[str] = None
    reason_for_visit: Optional[str] = None
    status: Optional[str] = "registered"
    created_by_user_id: Optional[int] = None


class VisitCreate(VisitBase):
    pass


class VisitUpdate(BaseModel):
    visit_date: Optional[datetime] = None
    referring_doctor: Optional[str] = None
    reason_for_visit: Optional[str] = None
    status: Optional[str] = None


class VisitOut(VisitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
