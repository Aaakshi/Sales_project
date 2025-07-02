from pydantic import BaseModel
from datetime import date

class SalesFileResponse(BaseModel):
    id: int
    filename: str
    upload_date: str

    class Config:
        from_attributes = True