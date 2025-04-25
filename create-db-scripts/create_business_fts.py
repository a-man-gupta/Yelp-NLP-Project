import sqlite3
import os

# Set up database path
db_folder = "../databases"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "business_data.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Make sure the base 'business' table exists
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

# Drop old FTS table if needed (optional safety reset)
cursor.execute("DROP TABLE IF EXISTS business_fts")

# Create new FTS5 table with content sync
cursor.execute("""
CREATE VIRTUAL TABLE business_fts USING fts5(
    name,
    address,
    city,
    content='business',
    content_rowid='rowid'
)
""")

# Rebuild the FTS index from the business table
cursor.execute("INSERT INTO business_fts(business_fts) VALUES('rebuild')")

# Save and close
conn.commit()
conn.close()

print("FTS5 table created and indexed successfully.")
