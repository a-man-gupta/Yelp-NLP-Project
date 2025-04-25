import sqlite3
import os

# Set up database path
db_folder = "../databases"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "users_data.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Make sure the base 'user' table exists
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

# Drop old FTS table if needed (optional)
cursor.execute("DROP TABLE IF EXISTS users_fts")

# Create new FTS5 table for user search
cursor.execute("""
CREATE VIRTUAL TABLE users_fts USING fts5(
    name,
    content='user',
    content_rowid='rowid'
)
""")

# Rebuild the FTS index from the user table
cursor.execute("INSERT INTO users_fts(users_fts) VALUES('rebuild')")

# Commit and close
conn.commit()
conn.close()

print("FTS5 table for users created and indexed successfully.")
