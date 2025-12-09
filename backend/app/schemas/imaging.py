from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class ImagingBase(BaseModel):
    patient_id: Optional[int] = None
    study_uid: Optional[str] = None
    modality: Optional[str] = None
    study_date: Optional[date] = None
    description: Optional[str] = None
    dicom_file_path: str
    source_device: Optional[str] = "Canon Xario 200"


class ImagingCreate(ImagingBase):
    pass


class ImagingUpdate(BaseModel):
    patient_id: Optional[int] = None
    description: Optional[str] = None


class ImagingOut(ImagingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
