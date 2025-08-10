# DBMS_HealthManagementSystem
This is a health care system that tracks the health of patients, based on past and current vitals. In case the vitals of a patient are about to shoot up and down, it will give an alert, the graph of individual and group vitals will also be displayed, for better reasoning.
#Steps to run the code:
1. Download the dataset from the following link and save it in HF_Data folder:
https://opendata.com.pk/dataset/the-heart-failure-prediction-pakistan/resource/cfb87734-bf91-4138-b48a-50fb68b1e2ce
Rename the file to Pak_Fais_HeartData.csv.

2. Run the DDL commands mentioned in SQL_structure.sql in MySQL workbench.

3. After that run the commands mention in insert_patients.sql

4. After that run the load_csv_to_mysql.py file to insert data into the SQL DB.

5. Open the Pre_Process folder, and run the data_prepare.py to get the data for model training.