from fastapi import FastAPI
from app.routers import sales, reports
from app.database import engine, Base
import logging
from cryptography.fernet import Fernet

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(title="Sales Data Aggregator & Report API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Sales Data Aggregator & Report API"}