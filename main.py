from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List, Optional
import uvicorn
import sqlite3

# Initialize FastAPI app
app = FastAPI(
    title="Schizophrenia Database API",
    description="API for CRUD Soperations on schizophrenia patient database",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    conn = sqlite3.connect('schizophrenia_dataset.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Helper functions for converting query results
def dict_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dict_fetch_one(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# Pydantic models for request validation
class PatientBase(BaseModel):
    Age: int
    Gender: int
    Education_Level: Optional[int] = None
    Marital_Status: Optional[int] = None
    Occupation: Optional[int] = None
    Income_Level: Optional[int] = None
    Live_Area: Optional[int] = None
    
    @validator('Age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
    
    @validator('Gender')
    def gender_valid_value(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError('Gender must be 0, 1, or 2')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "Age": 45,
                "Gender": 1,
                "Education_Level": 4,
                "Marital_Status": 1,
                "Occupation": 2,
                "Income_Level": 3,
                "Live_Area": 0
            }
        }

class PatientCreate(PatientBase):
    pass  # No additional fields needed for creation

class PatientResponse(PatientBase):
    Patient_ID: int
    
    class Config:
        from_attributes = True

class MedicalHistoryBase(BaseModel):
    Diagnosis: int
    Disease_Duration: Optional[int] = None
    Hospitalizations: Optional[int] = None
    Family_History: Optional[int] = None
    Substance_Use: Optional[int] = None
    Suicide_Attempt: Optional[int] = None
    Positive_Symptom_Score: Optional[int] = None
    Negative_Symptom_Score: Optional[int] = None
    GAF_Score: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "Diagnosis": 1,
                "Disease_Duration": 5,
                "Hospitalizations": 2,
                "Family_History": 0,
                "Substance_Use": 1,
                "Suicide_Attempt": 0,
                "Positive_Symptom_Score": 45,
                "Negative_Symptom_Score": 30,
                "GAF_Score": 65
            }
        }

class MedicalHistoryCreate(MedicalHistoryBase):
    Patient_ID: int

class MedicalHistoryResponse(MedicalHistoryBase):
    Patient_ID: int
    
    class Config:
        from_attributes = True

class SocialFactorsBase(BaseModel):
    Social_Support: Optional[int] = None
    Stress_Factors: Optional[int] = None
    Medication_Adherence: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "Social_Support": 2,
                "Stress_Factors": 3,
                "Medication_Adherence": 1
            }
        }

class SocialFactorsCreate(SocialFactorsBase):
    Patient_ID: int

class SocialFactorsResponse(SocialFactorsBase):
    Patient_ID: int
    
    class Config:
        from_attributes = True
