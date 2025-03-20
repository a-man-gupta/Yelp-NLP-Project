import json
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("tips_data.db")  # New database for tips
cursor = conn.cursor()

# Create table for tips data
cursor.execute("""
CREATE TABLE IF NOT EXISTS tip (
    user_id TEXT,
    business_id TEXT,
    text TEXT,
    date TEXT,
    compliment_count INTEGER,
    FOREIGN KEY (business_id) REFERENCES business(business_id)
)
""")

# Function to load tips data into the database
def load_tips_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:  # Process the JSON file line by line
            try:
                item = json.loads(line)  # Parse JSON object from each line
                user_id = item["user_id"]
                business_id = item["business_id"]
                text = item["text"]
                date = item["date"]
                compliment_count = item["compliment_count"]

                # Insert tip data into the database
                cursor.execute("""
                INSERT INTO tip (
                    user_id, business_id, text, date, compliment_count
                ) VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id, business_id, text, date, compliment_count
                ))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except sqlite3.ProgrammingError as e:
                print(f"Error inserting data into database: {e}")

# Load your tips JSON file into the database
load_tips_data("yelp_academic_dataset_tip.json")  # Replace with the actual JSON file path

# Commit changes and close connection
conn.commit()
conn.close()

print("Tips data has been loaded into the database successfully!")