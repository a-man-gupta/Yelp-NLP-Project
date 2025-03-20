import json
import sqlite3
import os

# Ensure the directory exists
db_folder = "../databases"  # Relative path to the databases folder from the script's location
os.makedirs(db_folder, exist_ok=True)

# Connect to SQLite database in the specified folder
db_path = os.path.join(db_folder, "reviews_data.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for reviews data
cursor.execute("""
CREATE TABLE IF NOT EXISTS review (
    review_id TEXT PRIMARY KEY,
    user_id TEXT,
    business_id TEXT,
    stars INTEGER,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date TEXT,
    FOREIGN KEY (business_id) REFERENCES business(business_id)
)
""")

# Function to load reviews data into the database
def load_reviews_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:  # Process the JSON file line by line
            try:
                item = json.loads(line)  # Parse JSON object from each line
                review_id = item["review_id"]
                user_id = item["user_id"]
                business_id = item["business_id"]
                stars = item["stars"]
                useful = item["useful"]
                funny = item["funny"]
                cool = item["cool"]
                text = item["text"]
                date = item["date"]

                # Insert review data into the database
                cursor.execute("""
                INSERT OR IGNORE INTO review (
                    review_id, user_id, business_id, stars, useful, funny,
                    cool, text, date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review_id, user_id, business_id, stars, useful, funny,
                    cool, text, date
                ))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except sqlite3.ProgrammingError as e:
                print(f"Error inserting data into database: {e}")

# Load your reviews JSON file into the database
load_reviews_data("../yelp_academic_dataset_review.json")  # Replace with the actual JSON file path

# Commit changes and close connection
conn.commit()
conn.close()

print("Reviews data has been loaded into the database successfully!")