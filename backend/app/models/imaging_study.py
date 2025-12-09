from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class ImagingStudy(Base):
    __tablename__ = "imaging_studies"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    study_uid = Column(String, unique=True, nullable=True)
    modality = Column(String, nullable=True)
    study_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    dicom_file_path = Column(Text, nullable=False)
    source_device = Column(Text, default="Canon Xario 200")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("Patient", back_populates="imaging_studies")
