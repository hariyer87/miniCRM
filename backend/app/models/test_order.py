from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class TestOrder(Base):
    __tablename__ = "test_orders"

    id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    test_catalog_id = Column(Integer, ForeignKey("test_catalog.id"), nullable=False)
    status = Column(String, default="ordered")
    sample_collected_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    visit = relationship("Visit", back_populates="test_orders")
    test_catalog = relationship("TestCatalog")
    result = relationship("TestResult", back_populates="test_order", uselist=False)
