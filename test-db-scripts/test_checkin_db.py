import sqlite3

# Connect to your database
conn = sqlite3.connect("checkin_data.db")  # Ensure you're using the correct database file
cursor = conn.cursor()

# Example: Query check-in data for a specific business_id
business_id = "---kPU91CF4Lq2-WlRu9Lw"  # Replace with the desired business ID
cursor.execute("SELECT date FROM checkin WHERE business_id = ?", (business_id,))

# Fetch and display results
results = cursor.fetchall()
print(f"Check-ins for business ID '{business_id}':")
for row in results:
    print(f"- {row[0]}")  # Each row contains a single 'date' entry

# Example: Count total check-ins for all businesses
cursor.execute("""
SELECT business_id, COUNT(*) AS total_checkins 
FROM checkin 
GROUP BY business_id 
ORDER BY total_checkins DESC 
LIMIT 10
""")
results = cursor.fetchall()
print("\nTop 10 businesses by total check-ins:")
for business_id, total_checkins in results:
    print(f"Business ID: {business_id}, Total Check-ins: {total_checkins}")

# Close connection
conn.close()