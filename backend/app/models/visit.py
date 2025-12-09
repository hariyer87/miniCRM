from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    referring_doctor = Column(String, nullable=True)
    reason_for_visit = Column(String, nullable=True)
    status = Column(String, default="registered")
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("Patient", back_populates="visits")
    test_orders = relationship("TestOrder", back_populates="visit")
    billing_record = relationship("BillingRecord", back_populates="visit", uselist=False)
