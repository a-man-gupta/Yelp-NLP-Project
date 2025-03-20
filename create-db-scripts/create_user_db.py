import json
import sqlite3
import os

# Ensure the directory exists
db_folder = "../databases"  # Relative path to the databases folder from the script's location
os.makedirs(db_folder, exist_ok=True)

# Connect to SQLite database in the specified folder
db_path = os.path.join(db_folder, "users_data.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for users data
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    review_count INTEGER,
    yelping_since TEXT,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    elite TEXT,
    friends TEXT
)
""")

# Function to load users data into the database
def load_users_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:  # Process the JSON file line by line
            try:
                item = json.loads(line)  # Parse JSON object from each line
                user_id = item["user_id"]
                name = item["name"]
                review_count = item["review_count"]
                yelping_since = item["yelping_since"]
                useful = item["useful"]
                funny = item["funny"]
                cool = item["cool"]
                elite = item.get("elite", None)  # Handle missing "elite" field gracefully
                friends = json.dumps(item.get("friends", None))  # Convert 'friends' field to JSON string

                # Insert user data into the database
                cursor.execute("""
                INSERT INTO user (
                    user_id, name, review_count, yelping_since, useful, funny,
                    cool, elite, friends
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id, name, review_count, yelping_since, useful, funny,
                    cool, elite, friends
                ))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except sqlite3.ProgrammingError as e:
                print(f"Error inserting data into database: {e}")

# Load your users JSON file into the database
load_users_data("../yelp_academic_dataset_user.json")  # Replace with the actual JSON file path

# Commit changes and close connection
conn.commit()
conn.close()

print("Users data has been loaded into the database successfully!")