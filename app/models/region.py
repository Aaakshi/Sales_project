from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)  # Specify length for MySQL
    sales_records = relationship("SalesRecord", back_populates="region_ref")