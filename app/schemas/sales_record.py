from pydantic import BaseModel

class SalesRecordCreate(BaseModel):
    date: str
    region: str
    product: str
    sales: float

class SalesRecordResponse(BaseModel):
    id: int
    date: str
    region: str
    product: str
    sales: float
    sales_file_id: int

    class Config:
        from_attributes = True