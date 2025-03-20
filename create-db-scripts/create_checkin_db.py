import json
import sqlite3
import os

# Ensure the directory exists
db_folder = "../databases"  # Relative path to the databases folder from the script's location
os.makedirs(db_folder, exist_ok=True)

# Connect to SQLite database in the specified folder
db_path = os.path.join(db_folder, "checkin_data.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for check-in data
cursor.execute("""
CREATE TABLE IF NOT EXISTS checkin (
    business_id TEXT,
    date TEXT,
    FOREIGN KEY (business_id) REFERENCES business(business_id)
)
""")

# Function to load check-in data into the database
def load_checkin_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:  # Process the JSON file line by line
            try:
                item = json.loads(line)  # Parse JSON object from each line
                business_id = item["business_id"]
                dates = item["date"].split(", ")  # Split the date string into a list

                for date in dates:  # Insert each date as a separate record
                    cursor.execute("""
                    INSERT INTO checkin (business_id, date)
                    VALUES (?, ?)
                    """, (business_id, date))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except sqlite3.ProgrammingError as e:
                print(f"Error inserting data into database: {e}")

# Load your check-in JSON file into the database
load_checkin_data("../yelp_academic_dataset_checkin.json")  # Replace with the actual JSON file path

# Commit changes and close connection
conn.commit()
conn.close()

print("Check-in data has been loaded into the database successfully!")