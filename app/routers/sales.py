from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.region import RegionResponse
from app.models.sales_file import SalesFile
from app.models.sales_record import SalesRecord
from app.models.region import Region
from app.schemas.sales_file import SalesFileResponse
from app.schemas.sales_record import SalesRecordCreate, SalesRecordResponse
from app.utils.csv_processor import process_csv
from app.database import get_db
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/upload-csv/", response_model=SalesFileResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    sales_file = await process_csv(file, db)
    return SalesFileResponse(
        id=sales_file.id,
        filename=sales_file.filename,
        upload_date=sales_file.upload_date.isoformat()
    )

@router.get("/files/", response_model=List[SalesFileResponse])
async def get_sales_files(db: Session = Depends(get_db)):
    files = db.query(SalesFile).all()
    return [SalesFileResponse(id=f.id, filename=f.filename, upload_date=f.upload_date.isoformat()) for f in files]

@router.get("/files/{file_id}", response_model=SalesFileResponse)
async def get_sales_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(SalesFile).filter(SalesFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return SalesFileResponse(id=file.id, filename=file.filename, upload_date=file.upload_date.isoformat())

@router.delete("/files/{file_id}")
async def delete_sales_file(file_id: int, db: Session = Depends( get_db)):
    file = db.query(SalesFile).filter(SalesFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(file)
    db.commit()
    return {"message": "File deleted successfully"}

@router.get("/records/", response_model=List[SalesRecordResponse])
async def get_sales_records(db: Session = Depends(get_db)):
    records = db.query(SalesRecord).all()
    return [SalesRecordResponse(
        id=r.id,
        date=r.date.isoformat(),
        region=r.region,
        product=r.product,
        sales=r.sales,
        sales_file_id=r.sales_file_id
    ) for r in records]

@router.get("/records/{record_id}", response_model=SalesRecordResponse)
async def get_sales_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(SalesRecord).filter(SalesRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return SalesRecordResponse(
        id=record.id,
        date=record.date.isoformat(),
        region=record.region,
        product=record.product,
        sales=record.sales,
        sales_file_id=record.sales_file_id
    )