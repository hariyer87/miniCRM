from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TestCatalogBase(BaseModel):
    code: str
    name: str
    sample_type: Optional[str] = None
    reference_range: Optional[str] = None
    turnaround_time_hours: Optional[int] = None
    price: Optional[float] = None
    is_active: bool = True


class TestCatalogCreate(TestCatalogBase):
    pass


class TestCatalogUpdate(BaseModel):
    name: Optional[str] = None
    sample_type: Optional[str] = None
    reference_range: Optional[str] = None
    turnaround_time_hours: Optional[int] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None


class TestCatalogOut(TestCatalogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
