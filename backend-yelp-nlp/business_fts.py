import sqlite3

# Path to your business database
db_path = "../databases/business_data.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign keys (optional but good practice)
cursor.execute("PRAGMA foreign_keys = ON;")

# Drop the FTS table if it already exists
cursor.execute("DROP TABLE IF EXISTS business_fts;")

# Step 1: Create the FTS5 virtual table
cursor.execute("""
CREATE VIRTUAL TABLE business_fts USING fts5(
  business_id UNINDEXED,
  name,
  content=''
);
""")

# Step 2: Populate it with data from the business table
cursor.execute("""
INSERT INTO business_fts (business_id, name)
SELECT business_id, name FROM business;
""")

# Commit and close
conn.commit()
conn.close()

print("FTS5 table created and populated successfully.")
