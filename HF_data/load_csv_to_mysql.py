import pandas as pd
import mysql.connector
from mysql.connector import Error

# ====== CONFIGURATION ======
CSV_FILE_PATH = "./HF_data/Pak_Fais_HeartData.csv"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "405658"
DB_NAME = "ai_health_prototype"
TABLE_NAME = "heart_data"

# ====== STEP 1: Read the CSV ======
df = pd.read_csv(CSV_FILE_PATH)

# OPTIONAL: Rename columns to match MySQL table exactly
# Example: If your table uses underscores instead of dots/spaces
rename_map = {
    "_id": "patient_id",
    "Age" : "age",
    "Age.Group": "age_group",
    "Gender" : "gender",
    "Locality": "locality",
    "Marital status": "marital_status",
    "Life.Style": "life_style",
    "Family.History": "family_history",
    "F.History": "f_history",
    "B.Urea": "b_urea",
    "S.Cr": "s_cr",
    "S.Sodium": "s_sodium",
    "S.Potassium": "s_potassium",
    "S.Chloride": "s_chloride",
    "C.P.K": "c_p_k",
    "CK.MB": "ck_mb",
    "P.C.V": "p_c_v",
    "M.C.V": "m_c_v",
    "M.C.H": "m_c_h",
    "M.C.H.C": "m_c_h_c",
    "PLATELET_COUNT": "platelet_count",
    "NEUTROPHIL": "neutrophil",
    "LYMPHO": "lympho",
    "MONOCYTE": "monocyte",
    "EOSINO": "eosino",
    "CO": "co",
    "Diagnosis": "diagnosis",
    "Hypersensitivity": "hypersensitivity",
    "SK": "sk",
    "SK.React": "sk_react",
    "Reaction": "reaction",
    "Mortality": "mortality",
    "Follow.Up": "follow_up"
}
df.rename(columns=rename_map, inplace=True)

# ====== STEP 2: Connect to MySQL ======
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        print("✅ Connected to MySQL database")

        cursor = connection.cursor()

        # Escape column names with backticks
        columns = ", ".join([f"`{col}`" for col in df.columns])
        placeholders = ", ".join(["%s"] * len(df.columns))

        # ====== STEP 3: Insert data row-by-row ======
        for _, row in df.iterrows():
            sql = f"INSERT INTO `{TABLE_NAME}` ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(row))

        connection.commit()
        print(f"✅ Inserted {len(df)} rows into `{TABLE_NAME}` table.")

except Error as e:
    print(f"❌ Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("🔌 MySQL connection closed")
