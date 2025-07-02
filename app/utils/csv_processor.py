from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.sales_file import SalesFile
from app.models.sales_record import SalesRecord
from app.models.region import Region
from datetime import datetime
import csv
from io import StringIO
import logging

logger = logging.getLogger(__name__)

async def process_csv(file: UploadFile, db: Session):
    content = await file.read()
    csv_file = StringIO(content.decode('utf-8'))
    reader = csv.DictReader(csv_file)
    
    if not all(col in reader.fieldnames for col in ['date', 'region', 'product', 'sales']):
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    
    sales_file = SalesFile(filename=file.filename)
    db.add(sales_file)
    db.commit()
    
    for row in reader:
        try:
            date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            region = db.query(Region).filter(Region.name == row['region']).first()
            if not region:
                region = Region(name=row['region'])
                db.add(region)
                db.commit()
            
            record = SalesRecord(
                date=date,
                region=row['region'],
                product=row['product'],
                sales=float(row['sales']),
                sales_file_id=sales_file.id,
                region_id=region.id
            )
            db.add(record)
        except Exception as e:
            logger.error(f"Error processing row: {e}")
            continue
    
    db.commit()
    return sales_file