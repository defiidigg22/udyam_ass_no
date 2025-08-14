# In main.py

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException # <--- NEW: Import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError # <--- NEW: Import IntegrityError
from pydantic import BaseModel, constr
from sqlalchemy.ext.declarative import declarative_base

# --- Database Setup (Unchanged) ---
DATABASE_URL = "postgresql://postgres:13271327@localhost/udyam_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Database Table Model (Unchanged) ---
class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    aadhaar_number = Column(String(12), unique=True, index=True)
    owner_name = Column(String, index=True)

Base.metadata.create_all(bind=engine)


# --- Pydantic Model (Unchanged) ---
class SubmissionCreate(BaseModel):
    aadhaar_number: constr(min_length=12, max_length=12)
    owner_name: str


# --- FastAPI Application ---
app = FastAPI()

# --- CORS Middleware (Unchanged) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- DB Dependency (Unchanged) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Root Endpoint (Unchanged) ---
@app.get("/")
def read_root():
    return {"message": "API is running. Submit form data to /submit"}


# --- Form Submission Endpoint (UPDATED) ---
@app.post("/submit/")
def create_submission(submission: SubmissionCreate, db: Annotated[Session, Depends(get_db)]):
    db_submission = Submission(
        aadhaar_number=submission.aadhaar_number,
        owner_name=submission.owner_name
    )
    
    try:
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        return db_submission
    except IntegrityError:
        # This block now catches the duplicate key error
        db.rollback() # Rollback the failed transaction
        raise HTTPException(
            status_code=400,
            detail="This Aadhaar number has already been submitted."
        )