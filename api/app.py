from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://airflow:airflow@postgres/airflow")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class ApiLog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String)
    records_count = Column(Integer)
    status = Column(String)
    response = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class BatchRequest(BaseModel):
    records: List[Dict[Any, Any]]

class BatchResponse(BaseModel):
    status: str
    message: str
    processed_records: int

# FastAPI app
app = FastAPI(title="Data Pipeline API")

@app.post("/api/v1/batch", response_model=BatchResponse)
async def process_batch(batch: BatchRequest):
    try:
        # Process the batch (in this example, we just log it)
        logger.info(f"Processing batch with {len(batch.records)} records")
        
        # Log to database
        db = SessionLocal()
        try:
            log_entry = ApiLog(
                batch_id=f"batch_{datetime.utcnow().timestamp()}",
                records_count=len(batch.records),
                status="success",
                response={"message": "Batch processed successfully"}
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            logger.error(f"Error logging to database: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail="Error logging batch")
        finally:
            db.close()

        return BatchResponse(
            status="success",
            message="Batch processed successfully",
            processed_records=len(batch.records)
        )
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 