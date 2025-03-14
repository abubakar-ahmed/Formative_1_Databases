# Schizophrenia Database
The Database 

## Overview
This project provides a FastAPI-based web service for managing a schizophrenia patient database. The API allows you to create, read, update, and delete patient records, medical histories, and social factors data.

## Database Schema

The database consists of three tables:  
1. **patients**  
2. **medical_history**  
3. **social_factors**  

### ERD Diagram  
Below is the **Entity-Relationship Diagram (ERD)** representing the database schema:  
---

## **Tables and Schema**

### 1. `patients` Table
Stores general patient information.

| Column Name      | Data Type | Description |
|-----------------|----------|-------------|
| `Patient_ID`    | INT (PK) | Unique ID for each patient |
| `Age`           | INT      | Patient's age |
| `Gender`        | INT      | Gender (0 = Female, 1 = Male) |
| `Education_Level` | INT    | Education level of the patient |
| `Marital_Status` | INT     | Marital status |
| `Occupation`    | INT      | Job type/category |
| `Income_Level`  | INT      | Income classification |
| `Live_Area`     | INT      | Area of residence |

---

### 2. `medical_history` Table
Stores patients' medical history details.

| Column Name             | Data Type | Description |
|------------------------|----------|-------------|
| `Patient_ID`          | INT (FK) | References `patients.Patient_ID` |
| `Diagnosis`           | INT      | Disease diagnosis code |
| `Disease_Duration`    | INT      | Duration of the disease in months |
| `Hospitalizations`    | INT      | Number of hospital admissions |
| `Family_History`      | INT      | Family history of the disease (0 = No, 1 = Yes) |
| `Substance_Use`       | INT      | History of substance use (0 = No, 1 = Yes) |
| `Suicide_Attempt`     | INT      | Any suicide attempt (0 = No, 1 = Yes) |
| `Positive_Symptom_Score` | INT   | Score for positive symptoms |
| `Negative_Symptom_Score` | INT   | Score for negative symptoms |
| `GAF_Score`          | INT      | Global Assessment of Functioning score |

---

### 3. `social_factors` Table
Stores social and psychological aspects affecting the patient.

| Column Name          | Data Type | Description |
|---------------------|----------|-------------|
| `Patient_ID`       | INT (FK) | References `patients.Patient_ID` |
| `Social_Support`   | INT      | Level of social support (0 = Low, 1 = High) |
| `Stress_Factors`   | INT      | Stress level (0 = Low, 2 = High) |
| `Medication_Adherence` | INT  | Adherence to medication (0 = Poor, 2 = Excellent) |


## Stored Procedure
A stored procedure to insert records into `Medical_History` to standardize data entry and maintain integrity.
```sql
DELIMITER $$
CREATE PROCEDURE InsertMedicalHistory(
    IN p_Patient_ID INT,
    IN p_Diagnosis INT,
    IN p_Disease_Duration INT,
    IN p_Hospitalizations INT
)
BEGIN
    INSERT INTO Medical_History (Patient_ID, Diagnosis, Disease_Duration, Hospitalizations)
    VALUES (p_Patient_ID, p_Diagnosis, p_Disease_Duration, p_Hospitalizations);
END $$
DELIMITER ;
```

## Trigger
A trigger that logs changes to patient records before updates occur.
```sql
DELIMITER $$
CREATE TRIGGER Before_Patient_Update
BEFORE UPDATE ON Patients
FOR EACH ROW
BEGIN
    INSERT INTO Change_Log (Patient_ID, Change_Time)
    VALUES (OLD.Patient_ID, NOW());
END $$
DELIMITER ;
```

## ERD Diagram
An Entity-Relationship Diagram (ERD) visually represents the database schema and relationships between tables. The ERD diagram is included in the project folder

## API Live Deployment
The API is deployed and accessible at: [https://formative-1-databases.onrender.com]
You can interact with the API documentation at:
- Swagger UI: [https://formative-1-databases.onrender.com/docs]
- ReDoc: [https://formative-1-databases.onrender.com/redoc]

## Database Schema
The database consists of three main tables:
1. **Patients**
- Patient_ID (Primary Key, Auto-increment)
- Age
- Gender
- Education_Level
- Marital_Status
- Occupation
- Income_Level
- Live_Area

2. **Medical_History**
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

3. **Social_Factors**
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
   ``` bash
   git clone https://github.com/yourusername/schizophrenia-database-api.git
   cd schizophrenia-database-api
   ```
2. Create a virtual environment
   ``` bash
   python -m venv env
   source env/bin/activate  # On Windows, use: env\Scripts\activate
   ```
3. Install dependencies
   ``` bash
   pip install fastapi uvicorn sqlite3 pydantic
   ```
4. Create the database directory
   ``` bash
   mkdir -p persistent_data
   ```
5. Initialize the database
   ``` bash
   python init_db.py
   ```

## Running the API Locally
Start the server with:
``` bash
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
