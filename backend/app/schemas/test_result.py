from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TestResultBase(BaseModel):
    test_order_id: int
    result_value: Optional[str] = None
    units: Optional[str] = None
    reference_range: Optional[str] = None
    comment: Optional[str] = None
    status: Optional[str] = "draft"
    finalized_by_user_id: Optional[int] = None
    finalized_at: Optional[datetime] = None


class TestResultCreate(TestResultBase):
    pass


class TestResultUpdate(BaseModel):
    result_value: Optional[str] = None
    units: Optional[str] = None
    reference_range: Optional[str] = None
    comment: Optional[str] = None
    status: Optional[str] = None


class TestResultOut(TestResultBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
