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

# Create main business table
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
        for line in f:
            try:
                item = json.loads(line)
                attributes = json.dumps(item.get("attributes", {}))
                categories = item.get("categories", None)
                hours = json.dumps(item.get("hours", None))

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

# Load the data
load_data("yelp_academic_dataset_business.json")

# Create FTS5 table for business search
cursor.execute("""
CREATE VIRTUAL TABLE IF NOT EXISTS business_fts USING fts5(
    business_id UNINDEXED,
    name,
    address,
    city,
    content=''
)
""")

# Populate FTS table from main business table
cursor.execute("DELETE FROM business_fts")  # Clear old data if any
cursor.execute("""
INSERT INTO business_fts (business_id, name, address, city)
SELECT business_id, name, address, city FROM business
""")

# Finalize
conn.commit()
conn.close()

print("Business data loaded and FTS5 index created successfully!")
