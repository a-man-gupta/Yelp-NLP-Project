import json
import sqlite3
import os

# Ensure the directory exists
db_folder = "../databases"  # Relative path to the databases folder from the script's location
os.makedirs(db_folder, exist_ok=True)

# Connect to SQLite database in the specified folder
db_path = os.path.join(db_folder, "business_data.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables based on the schema
cursor.execute("""
CREATE TABLE IF NOT EXISTS business (
    business_id TEXT PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    latitude REAL,
    longitude REAL,
    stars INTEGER,
    review_count INTEGER,
    is_open INTEGER,
    attributes TEXT,
    categories TEXT,
    hours TEXT
)
""")

# Function to load JSON into database
def load_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:  # Process the JSON file line by line
            try:
                item = json.loads(line)  # Parse JSON object from each line
                # Convert 'attributes' dictionary to JSON string
                attributes = json.dumps(item.get("attributes", {}))  
                # Handle other fields as-is or set to None if missing
                categories = item.get("categories", None)
                hours = json.dumps(item.get("hours", None))  # Convert to JSON string if needed

                # Insert into SQLite database
                cursor.execute("""
                INSERT OR IGNORE INTO business (
                    business_id, name, address, city, state, postal_code,
                    latitude, longitude, stars, review_count, is_open,
                    attributes, categories, hours
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item["business_id"], item["name"], item["address"], item["city"],
                    item["state"], item["postal_code"], item["latitude"],
                    item["longitude"], item["stars"], item["review_count"],
                    item["is_open"], attributes, categories, hours
                ))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except sqlite3.ProgrammingError as e:
                print(f"Error inserting data into database: {e}")

# Load your JSON file into the database
load_data("../yelp_academic_dataset_business.json")  # Replace with the actual JSON file path

# Commit changes and close connection
conn.commit()
conn.close()

print("Data has been loaded into the database successfully!")
