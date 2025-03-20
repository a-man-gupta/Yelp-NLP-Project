import sqlite3

# Connect to your tips database
conn = sqlite3.connect("tips_data.db")  # Ensure you're using the correct database file
cursor = conn.cursor()

# Example: Query tips for a specific business_id
business_id = "3uLgwr0qeCNMjKenHJwPGQ"  # Replace with the desired business ID
cursor.execute("SELECT text, date, compliment_count FROM tip WHERE business_id = ?", (business_id,))

# Fetch and display results
results = cursor.fetchall()
print(f"Tips for business ID '{business_id}':")
for text, date, compliment_count in results:
    print(f"Date: {date}, Compliment Count: {compliment_count}\nTip: {text}\n")

# Example: Find the most complimented tips
cursor.execute("""
SELECT text, compliment_count, date 
FROM tip 
ORDER BY compliment_count DESC 
LIMIT 5
""")
results = cursor.fetchall()
print("\nTop 5 most complimented tips:")
for text, compliment_count, date in results:
    print(f"Date: {date}, Compliments: {compliment_count}\nTip: {text}\n")

# Example: Retrieve users who left tips for a specific business
cursor.execute("SELECT user_id FROM tip WHERE business_id = ?", (business_id,))
results = cursor.fetchall()
print("\nUsers who left tips for business ID '{business_id}':")
for row in results:
    print(f"- User ID: {row[0]}")

# Close connection
conn.close()