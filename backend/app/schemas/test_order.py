from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TestOrderBase(BaseModel):
    visit_id: int
    test_catalog_id: int
    status: Optional[str] = "ordered"
    sample_collected_at: Optional[datetime] = None


class TestOrderCreate(TestOrderBase):
    pass


class TestOrderUpdate(BaseModel):
    status: Optional[str] = None
    sample_collected_at: Optional[datetime] = None


class TestOrderOut(TestOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
