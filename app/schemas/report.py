from pydantic import BaseModel

class MonthlyReport(BaseModel):
    region: str
    month: str
    total_sales: float