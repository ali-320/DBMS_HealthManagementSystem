import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Step 1: Configuration and DB Connection
DB_USER = "root"
DB_PASSWORD = "405658"  # Move to .env for security
DB_HOST = "localhost"
DB_NAME = "ai_health_prototype"
engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

# Features for unsupervised anomaly detection (vitals/labs - numeric only)
unsupervised_features = [
    'bp', 'thrombolysis', 'trestbps', 'c_p_k', 'ck_mb',
    's_cr', 's_sodium', 'platelet_count',
    'bgr', 'b_urea', 's_potassium', 's_chloride',
    'esr', 'wbc', 'rbc', 'hemoglobin', 'p_c_v',
    'm_c_v', 'm_c_h', 'm_c_h_c', 'neutrophil', 'lympho',
    'monocyte', 'eosino', 'cp', 'chol', 'fbs', 'restecg',
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal',
    'num', 'sk', 'reaction', 'follow_up'
]

# Additional features for supervised (include categoricals)
supervised_features = unsupervised_features + [
    'age', 'gender', 'diabetes', 'smoking', 'htn',
    'marital_status', 'hyperlipi', 'depression',
    'category', 'hypersensitivity', 'f_history'
]


# Step 2: Query Data
query = f"""
SELECT data_id, patient_id, mortality, 
       {', '.join(supervised_features)} 
FROM heart_data
"""
df = pd.read_sql(query, engine)

# Step 3: Separate for Unsupervised and Supervised
# For Unsupervised: Only numeric features (add categoricals if needed later)
df_unsupervised = df[['data_id', 'patient_id'] + unsupervised_features].copy()

# For Supervised: All features + target
df_supervised = df[['data_id', 'patient_id'] + supervised_features + ['mortality']].copy()
X_sup = df_supervised[supervised_features]
y_sup = df_supervised['mortality']

# Step 4: Preprocessing Pipelines
# Unsupervised Pipeline (impute + scale numerics)
unsupervised_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
X_unsupervised = unsupervised_pipeline.fit_transform(df_unsupervised[unsupervised_features])

# Supervised Pipeline (impute + scale numerics, encode categoricals)
numeric_features = [
    # Core vitals/labs
    'bp', 'trestbps', 'c_p_k', 'ck_mb', 's_cr', 's_sodium', 'platelet_count',
    'bgr', 'b_urea', 's_potassium', 's_chloride',
    'esr', 'wbc', 'rbc', 'hemoglobin', 'p_c_v',
    'm_c_v', 'm_c_h', 'm_c_h_c', 'neutrophil', 'lympho', 'monocyte', 'eosino',
    
    # Heart-specific metrics
    'cp', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak',
    'slope', 'ca', 'thal', 'num',
    
    # Outcomes & reaction
    'sk', 'reaction', 'follow_up',
    
    # Demographics & history (numeric)
    'age', 'diabetes', 'f_history'
]

categorical_features = [
    'gender', 'smoking', 'htn', 'marital_status', 'hyperlipi', 'depression',
    'category', 'hypersensitivity'
]


preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numeric_features),
        ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('encoder', OneHotEncoder(handle_unknown='ignore'))]), categorical_features)
    ]
)
X_sup_preprocessed = preprocessor.fit_transform(X_sup)

# Step 5: Train/Test Split for Supervised (80/20, stratified)
X_train, X_test, y_train, y_test = train_test_split(X_sup_preprocessed, y_sup, test_size=0.2, stratify=y_sup, random_state=42)

# Outputs
print(f"Unsupervised ready: X shape {X_unsupervised.shape}")
print(f"Supervised ready: X_train shape {X_train.shape}, y_train shape {y_train.shape}")

# Save prepared data if needed (e.g., for later training)
pd.DataFrame(X_unsupervised, columns=unsupervised_features).to_csv('./Pre_Process/prepared_unsupervised.csv', index=False)
pd.DataFrame(X_train).to_csv('./Pre_Process/X_train_sup.csv', index=False)  # Note: Columns are transformed
y_train.to_csv('./Pre_Process/y_train_sup.csv', index=False)

# Supervised test
pd.DataFrame(X_test).to_csv('./Pre_Process/X_test.csv', index=False)    # transformed columns
y_test.to_csv('./Pre_Process/y_test.csv', index=False)