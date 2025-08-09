-- ===========================================
-- Database: AI Health Prototype
-- Author: Ali (NUST) - Optimized by GPT-5
-- Purpose: Store heart health patient data 
--          for AI model training & anomaly detection
-- ===========================================

CREATE DATABASE IF NOT EXISTS ai_health_prototype;
USE ai_health_prototype;

-- ========================
-- Table: patients
-- Core patient identifiers
-- ========================
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,        -- Use CSV "_id" here (external system ID)
    age DECIMAL(5,2) CHECK (age >= 0), -- Age in years, allow decimals
    gender ENUM('Male', 'Female', 'Other', 'Unknown') DEFAULT 'Unknown',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Index for age-based queries (e.g., risk stratification)
CREATE INDEX idx_patients_age ON patients(age);


-- ========================
-- Table: heart_data
-- Detailed medical & lab info
-- ========================
CREATE TABLE heart_data (
    data_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    
    -- Demographics
    age_group VARCHAR(50),
    locality VARCHAR(255),
    marital_status ENUM('Single', 'Married', 'Divorced', 'Widowed', 'Unknown') DEFAULT 'Unknown',
    life_style TEXT,
    sleep VARCHAR(50),
    
    -- Medical history
    category VARCHAR(255),
    depression VARCHAR(50),
    hyperlipi VARCHAR(50),
    smoking ENUM('Yes', 'No', 'Former', 'Unknown') DEFAULT 'Unknown',
    family_history TEXT,
    f_history DECIMAL(5,2),
    diabetes DECIMAL(5,2),
    htn VARCHAR(50),
    allergies VARCHAR(255),
    
    -- Vitals & Lab results
    bp DECIMAL(6,2),
    thrombolysis DECIMAL(6,2),
    bgr DECIMAL(6,2),
    b_urea DECIMAL(6,2),
    s_cr DECIMAL(6,2),
    s_sodium DECIMAL(6,2),
    s_potassium DECIMAL(6,2),
    s_chloride DECIMAL(6,2),
    c_p_k DECIMAL(6,2),
    ck_mb DECIMAL(6,2),
    esr DECIMAL(6,2),
    wbc DECIMAL(8,2),
    rbc DECIMAL(8,2),
    hemoglobin DECIMAL(5,2),
    p_c_v DECIMAL(5,2),
    m_c_v DECIMAL(5,2),
    m_c_h DECIMAL(5,2),
    m_c_h_c DECIMAL(5,2),
    platelet_count DECIMAL(10,2),
    neutrophil DECIMAL(5,2),
    lympho DECIMAL(5,2),
    monocyte DECIMAL(5,2),
    eosino DECIMAL(5,2),
    
    -- Diagnostics
    others TEXT,
    co TEXT,
    diagnosis TEXT,
    hypersensitivity VARCHAR(255),
    
    -- Heart-specific test results
    cp DECIMAL(5,2),
    trestbps DECIMAL(6,2),
    chol DECIMAL(6,2),
    fbs DECIMAL(5,2),
    restecg DECIMAL(5,2),
    thalach DECIMAL(5,2),
    exang DECIMAL(5,2),
    oldpeak DECIMAL(5,2),
    slope DECIMAL(5,2),
    ca DECIMAL(5,2),
    thal DECIMAL(5,2),
    num DECIMAL(5,2),
    
    -- Allergy & reaction data
    sk DECIMAL(5,2),
    sk_react VARCHAR(255),
    reaction DECIMAL(5,2),
    
    -- Outcomes
    mortality DECIMAL(5,2),
    follow_up DECIMAL(5,2),
    
    -- Foreign key to patients
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Performance indexes
CREATE INDEX idx_heart_data_patient_id ON heart_data(patient_id);
CREATE INDEX idx_heart_data_mortality ON heart_data(mortality);
CREATE INDEX idx_heart_data_diagnosis ON heart_data(diagnosis(100));


-- ========================
-- Table: model_registry
-- Tracks ML models for reproducibility
-- ========================
CREATE TABLE model_registry (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    artifact_path VARCHAR(255) NOT NULL, -- Path to saved model file
    metrics JSON,                        -- Training/testing metrics
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- ========================
-- Table: anomaly_alerts
-- Stores AI-detected anomalies
-- ========================
CREATE TABLE anomaly_alerts (
    alert_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    model_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    anomaly_score DECIMAL(6,3) CHECK (anomaly_score >= 0),
    details JSON, -- Additional anomaly metadata
    acknowledged TINYINT(1) DEFAULT 0,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES model_registry(model_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_anomaly_patient_id ON anomaly_alerts(patient_id);
CREATE INDEX idx_anomaly_model_id ON anomaly_alerts(model_id);
