from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.session import Base


class BillingRecord(Base):
    __tablename__ = "billing_records"

    id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False, unique=True)
    subtotal_amount = Column(Numeric, nullable=True, default=0)
    discount_amount = Column(Numeric, nullable=True, default=0)
    total_amount = Column(Numeric, nullable=True, default=0)
    amount_paid = Column(Numeric, nullable=True, default=0)
    balance_amount = Column(Numeric, nullable=True, default=0)
    payment_mode = Column(String, nullable=True)
    status = Column(String, default="unpaid")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    visit = relationship("Visit", back_populates="billing_record")
