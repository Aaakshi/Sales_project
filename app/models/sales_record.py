from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SalesRecord(Base):
    __tablename__ = "sales_records"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    region = Column(String(100))
    product = Column(String(100))
    sales = Column(Float)
    sales_file_id = Column(Integer, ForeignKey("sales_files.id"))
    sales_file = relationship("SalesFile", back_populates="records")
    region_id = Column(Integer, ForeignKey("regions.id"))
    region_ref = relationship("Region", back_populates="sales_records")