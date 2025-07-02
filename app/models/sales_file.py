from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class SalesFile(Base):
    __tablename__ = "sales_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)  # Specify length for MySQL
    upload_date = Column(Date, default=datetime.utcnow)
    records = relationship("SalesRecord", back_populates="sales_file")