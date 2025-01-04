import sqlite3
import pandas as pd

# Define the paths for your CSV and database
csv_file_path = 'expert_profiles_all.csv'  # Same folder as this script
db_file_path = 'experts.db'  # Database will also be in the data folder

# Connect to SQLite Database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create the expert_profiles table
create_table_query = '''
CREATE TABLE IF NOT EXISTS expert_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    label TEXT,
    profile TEXT,
    url TEXT
);
'''
cursor.execute(create_table_query)

# Load CSV into a DataFrame
df = pd.read_csv(csv_file_path)

# Insert data into the database
df.to_sql('expert_profiles', conn, if_exists='replace', index=False)

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database '{db_file_path}' populated successfully with data from '{csv_file_path}'.")
