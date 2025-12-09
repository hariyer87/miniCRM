from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True)
    test_order_id = Column(Integer, ForeignKey("test_orders.id"), unique=True, nullable=False)
    result_value = Column(Text, nullable=True)
    units = Column(String, nullable=True)
    reference_range = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    status = Column(String, default="draft")
    finalized_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    finalized_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    test_order = relationship("TestOrder", back_populates="result")
