import sqlite3

conn = sqlite3.connect("../databases/business_data.db")
cursor = conn.cursor()

search_term = "coffee"  # Try other words too

cursor.execute("""
SELECT b.business_id, b.name, b.city
FROM business_fts f
JOIN business b ON b.rowid = f.rowid
WHERE f.name MATCH ?
LIMIT 10
""", (search_term,))

results = cursor.fetchall()

print(f"\nTop results for '{search_term}':")
for row in results:
    print(row)

conn.close()
