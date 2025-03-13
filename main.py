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

# Patients Collection Routes
@app.post("/patients/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED, tags=["Patients"])
async def create_patient(patient: PatientBase, db = Depends(get_db)):
    """
    Create a new patient record.
    """
    cursor = db.cursor()
    try:
        # Insert patient record
        query = """
        INSERT INTO Patients (Age, Gender, Education_Level, Marital_Status, Occupation, Income_Level, Live_Area)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            patient.Age,
            patient.Gender,
            patient.Education_Level,
            patient.Marital_Status,
            patient.Occupation,
            patient.Income_Level,
            patient.Live_Area
        )
        
        cursor.execute(query, values)
        db.commit()
        
        # Get the auto-generated ID
        patient_id = cursor.lastrowid
        
        # Fetch the created patient
        cursor.execute("SELECT * FROM Patients WHERE Patient_ID = ?", (patient_id,))
        new_patient = dict_fetch_one(cursor)
        
        return new_patient
    except sqlite3.Error as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(err)}")
    finally:
        cursor.close()

@app.get("/patients/", response_model=List[PatientResponse], tags=["Patients"])
async def read_patients(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    """
    Retrieve all patients with pagination.
    """
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM Patients LIMIT ? OFFSET ?", (limit, skip))
        patients = dict_fetch_all(cursor)
        return patients
    except sqlite3.Error as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(err)}")
    finally:
        cursor.close()

@app.get("/patients/{patient_id}", response_model=PatientResponse, tags=["Patients"])
async def read_patient(patient_id: int, db = Depends(get_db)):
    """
    Retrieve a specific patient by ID.
    """
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM Patients WHERE Patient_ID = ?", (patient_id,))
        patient = dict_fetch_one(cursor)
        
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID {patient_id} not found")
        
        return patient
    except sqlite3.Error as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(err)}")
    finally:
        cursor.close()

@app.put("/patients/{patient_id}", response_model=PatientResponse, tags=["Patients"])
async def update_patient(patient_id: int, patient: PatientBase, db = Depends(get_db)):
    """
    Update a patient record.
    """
    cursor = db.cursor()
    try:
        # Check if patient exists
        cursor.execute("SELECT * FROM Patients WHERE Patient_ID = ?", (patient_id,))
        if dict_fetch_one(cursor) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID {patient_id} not found")
        
        # Update patient
        query = """
        UPDATE Patients 
        SET Age = ?, Gender = ?, Education_Level = ?, Marital_Status = ?, 
            Occupation = ?, Income_Level = ?, Live_Area = ? 
        WHERE Patient_ID = ?
        """
        values = (
            patient.Age,
            patient.Gender,
            patient.Education_Level,
            patient.Marital_Status,
            patient.Occupation,
            patient.Income_Level,
            patient.Live_Area,
            patient_id
        )
        
        cursor.execute(query, values)
        db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="Patient data was not modified")
        
        # Return updated patient
        cursor.execute("SELECT * FROM Patients WHERE Patient_ID = ?", (patient_id,))
        updated_patient = dict_fetch_one(cursor)
        
        return updated_patient
    except sqlite3.Error as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(err)}")
    finally:
        cursor.close()

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Patients"])
async def delete_patient(patient_id: int, db = Depends(get_db)):
    """
    Delete a patient record.
    """
    cursor = db.cursor()
    try:
        # Check if patient exists
        cursor.execute("SELECT * FROM Patients WHERE Patient_ID = ?", (patient_id,))
        if dict_fetch_one(cursor) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID {patient_id} not found")
        
        # Delete related data first due to foreign key constraints
        cursor.execute("DELETE FROM Social_Factors WHERE Patient_ID = ?", (patient_id,))
        cursor.execute("DELETE FROM Medical_History WHERE Patient_ID = ?", (patient_id,))
        
        # Delete patient
        cursor.execute("DELETE FROM Patients WHERE Patient_ID = ?", (patient_id,))
        db.commit()
        
        return None
    except sqlite3.Error as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(err)}")
    finally:
        cursor.close()
