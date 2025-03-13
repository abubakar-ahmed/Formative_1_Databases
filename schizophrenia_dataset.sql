use schizophrenia_dataset;

DROP TABLE IF EXISTS Medical_History;
DROP TABLE IF EXISTS Social_Factors;
DROP TABLE IF EXISTS Patients;
CREATE TABLE Patients (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
    Age INT,
    Gender INT,
    Education_Level INT,
    Marital_Status INT,
    Occupation INT,
    Income_Level INT,
    Live_Area INT
);

CREATE TABLE Medical_History (
    Patient_ID INT AUTO_INCREMENT,
    Diagnosis INT,
    Disease_Duration INT,
    Hospitalizations INT,
    Family_History INT,
    Substance_Use INT,
    Suicide_Attempt INT,
    Positive_Symptom_Score INT,
    Negative_Symptom_Score INT,
    GAF_Score INT,
    FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID)
);

CREATE TABLE Social_Factors (
    Patient_ID INT AUTO_INCREMENT,
    Social_Support INT,
    Stress_Factors INT,
    Medication_Adherence INT,
    FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID)
);

DROP PROCEDURE IF EXISTS InsertMedicalHistory;
DELIMITER //
CREATE PROCEDURE InsertMedicalHistory(
    IN p_Patient_ID INT, 
    IN p_Diagnosis INT, 
    IN p_Disease_Duration INT,
    IN p_Hospitalizations INT
)
BEGIN
    INSERT INTO Medical_History (Patient_ID, Diagnosis, Disease_Duration, Hospitalizations) 
    VALUES (p_Patient_ID, p_Diagnosis, p_Disease_Duration, p_Hospitalizations);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER ValidateAgeBeforeInsert
BEFORE INSERT ON Patients
FOR EACH ROW
BEGIN
    IF NEW.Age < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Age cannot be negative!';
    END IF;
END //
DELIMITER ;

