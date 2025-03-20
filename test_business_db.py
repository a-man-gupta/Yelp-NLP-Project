import sqlite3

# Connect to your database
conn = sqlite3.connect("business_data.db")
cursor = conn.cursor()

# Example: Query businesses in a specific city
city = "Santa Barbara"
cursor.execute("SELECT name, address FROM business WHERE city = ?", (city,))

# Fetch and display results
results = cursor.fetchall()
for name, address in results:
    print(f"Name: {name}, Address: {address}")

# Close connection
conn.close()