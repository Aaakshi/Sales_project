from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.sales_record import SalesRecord
from app.models.region import Region
from app.schemas.report import MonthlyReport
from app.schemas.region import RegionResponse
from app.database import get_db
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/monthly/", response_model=List[MonthlyReport])
async def get_monthly_report(year: int, db: Session = Depends(get_db)):
    results = db.query(
        SalesRecord.region,
        func.date_format(SalesRecord.date, '%Y-%m').label('month'),  # Changed to date_format
        func.sum(SalesRecord.sales).label('total_sales')
    ).group_by(SalesRecord.region, func.date_format(SalesRecord.date, '%Y-%m')
    ).filter(func.year(SalesRecord.date) == year).all()  # Changed to func.year
    
    return [MonthlyReport(region=r[0], month=r[1], total_sales=r[2]) for r in results]

@router.get("/regional/", response_model=List[MonthlyReport])
async def get_regional_report(region: str, db: Session = Depends(get_db)):
    results = db.query(
        SalesRecord.region,
        func.date_format(SalesRecord.date, '%Y-%m').label('month'),  # Changed to date_format
        func.sum(SalesRecord.sales).label('total_sales')
    ).filter(SalesRecord.region == region
    ).group_by(SalesRecord.region, func.date_format(SalesRecord.date, '%Y-%m')).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Region not found")
    return [MonthlyReport(region=r[0], month=r[1], total_sales=r[2]) for r in results]

@router.get("/product-sales/", response_model=List[MonthlyReport])
async def get_product_sales(product: str, db: Session = Depends(get_db)):
    results = db.query(
        SalesRecord.region,
        func.date_format(SalesRecord.date, '%Y-%m').label('month'),  # Changed to date_format
        func.sum(SalesRecord.sales).label('total_sales')
    ).filter(SalesRecord.product == product
    ).group_by(SalesRecord.region, func.date_format(SalesRecord.date, '%Y-%m')).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Product not found")
    return [MonthlyReport(region=r[0], month=r[1], total_sales=r[2]) for r in results]

@router.get("/top-regions/", response_model=List[RegionResponse])
async def get_top_regions(limit: int = 5, db: Session = Depends(get_db)):
    results = db.query(
        Region.name,
        Region.id
    ).join(SalesRecord).group_by(Region.id, Region.name
    ).order_by(func.sum(SalesRecord.sales).desc()).limit(limit).all()
    
    return [RegionResponse(id=r[1], name=r[0]) for r in results]