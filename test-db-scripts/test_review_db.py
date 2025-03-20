
import sqlite3

# Connect to your reviews database
conn = sqlite3.connect("../databases/reviews_data.db")  # Ensure you're using the correct database file
cursor = conn.cursor()

# Example 1: Query all reviews for a specific business ID
business_id = "XQfwVwDr-v0ZS3_CbbE5Xw"  # Replace with your desired business ID
cursor.execute("SELECT stars, text, date FROM review WHERE business_id = ?", (business_id,))

# Fetch and display results
results = cursor.fetchall()
print(f"Reviews for business ID '{business_id}':")
for stars, text, date in results:
    print(f"Stars: {stars}, Date: {date}\nReview: {text}\n")

# Example 2: Find the average star rating for a specific business
cursor.execute("SELECT AVG(stars) AS average_rating FROM review WHERE business_id = ?", (business_id,))
average_rating = cursor.fetchone()[0]
print(f"Average rating for business ID '{business_id}': {average_rating:.2f}")

# Example 3: Retrieve the top 5 most useful reviews
cursor.execute("""
SELECT review_id, useful, text 
FROM review 
ORDER BY useful DESC 
LIMIT 5
""")
results = cursor.fetchall()
print("\nTop 5 most useful reviews:")
for review_id, useful, text in results:
    print(f"Review ID: {review_id}, Useful: {useful}\nReview: {text}\n")

# Close connection
conn.close()
