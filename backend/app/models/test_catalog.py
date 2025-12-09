from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric
from app.db.session import Base


class TestCatalog(Base):
    __tablename__ = "test_catalog"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    sample_type = Column(String, nullable=True)
    reference_range = Column(Text, nullable=True)
    turnaround_time_hours = Column(Integer, nullable=True)
    price = Column(Numeric, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
