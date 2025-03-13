# Schizophrenia Database
The Database 

## Overview
This project provides a FastAPI-based web service for managing a schizophrenia patient database. The API allows you to create, read, update, and delete patient records, medical histories, and social factors data.

## API Live Deployment
The API is deployed and accessible at: [https://formative-1-databases.onrender.com]
You can interact with the API documentation at:
- Swagger UI: [https://formative-1-databases.onrender.com/docs]
- ReDoc: [https://formative-1-databases.onrender.com/redoc]

## Database Schema
The database consists of three main tables:
1. Patients
- Patient_ID (Primary Key, Auto-increment)
- Age
- Gender
- Education_Level
- Marital_Status
- Occupation
- Income_Level
- Live_Area

2. Medical_History
- Patient_ID (Foreign Key)
- Diagnosis
- Disease_Duration
- Hospitalizations
- Family_History
- Substance_Use
- Suicide_Attempt
- Positive_Symptom_Score
- Negative_Symptom_Score
- GAF_Score

3. Social_Factors
- Patient_ID (Foreign Key)
- Social_Support
- Stress_Factors
- Medication_Adherence

## Technical Stack

- **FastAPI:** Modern, fast web framework for building APIs with Python
- **SQLite:** Lightweight database for storing patient data
- **Pydantic:** Data validation and settings management
- **Uvicorn:** ASGI server for running the API locally

## Installation
1. Clone the repository
   ```
   git clone https://github.com/yourusername/schizophrenia-database-api.git
   cd schizophrenia-database-api
   ```
2. Create a virtual environment
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use: env\Scripts\activate
   ```
3. Install dependencies
   ```
   pip install fastapi uvicorn sqlite3 pydantic
   ```
4. Create the database directory
   ```
   mkdir -p persistent_data
   ```
5. Initialize the database
   ```
   python init_db.py
   ```

## Running the API Locally
Start the server with:
```
uvicorn main:app --reload
```
The API will be available at [http://127.0.0.1:8000]

## API Endpoints
### Patients
- `POST /patients/` - Create a new patient
- `GET /patients/` - List all patients
- `GET /patients/{patient_id}` - Get a specific patient
- `PUT /patients/{patient_id}` - Update a patient
- `DELETE /patients/{patient_id}` - Delete a patient
### Medical History
- `POST /medical-history/` - Create a medical history record
- `GET /medical-history/` - List all medical history records
- `GET /medical-history/{patient_id}` - Get medical history for a specific patient
- `PUT /medical-history/{patient_id}` - Update medical history
- `DELETE /medical-history/{patient_id}` - Delete medical history
### Social Factors
- `POST /social-factors/` - Create a social factors record
- `GET /social-factors/` - List all social factors records
- `GET /social-factors/{patient_id}` - Get social factors for a specific patient
- `PUT /social-factors/{patient_id}` - Update social factors
- `DELETE /social-factors/{patient_id}` - Delete social factors
### Aggregated Data
- `GET /patient-complete/{patient_id}` - Get complete patient data including medical history and social factors

## Example Usage
### Creating a Patient
```
curl -X 'POST' \
  'https://formative-1-databases.onrender.com/patients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "Age": 45,
  "Gender": 1,
  "Education_Level": 4,
  "Marital_Status": 1,
  "Occupation": 2,
  "Income_Level": 3,
  "Live_Area": 0
}'
```
### Adding Medical History
```
curl -X 'POST' \
  'https://formative-1-databases.onrender.com/medical-history/' \
  -H 'Content-Type: application/json' \
  -d '{
  "Patient_ID": 1,
  "Diagnosis": 1,
  "Disease_Duration": 5,
  "Hospitalizations": 2,
  "Family_History": 0,
  "Substance_Use": 1,
  "Suicide_Attempt": 0,
  "Positive_Symptom_Score": 45,
  "Negative_Symptom_Score": 30,
  "GAF_Score": 65
}'
```
### Adding Social Factors
```
curl -X 'POST' \
  'https://formative-1-databases.onrender.com/social-factors/' \
  -H 'Content-Type: application/json' \
  -d '{
  "Patient_ID": 1,
  "Social_Support": 2,
  "Stress_Factors": 3,
  "Medication_Adherence": 1
}'
```
