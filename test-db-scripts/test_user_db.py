import sqlite3

# Connect to your users database
conn = sqlite3.connect("users_data.db")  # Ensure you're using the correct database file
cursor = conn.cursor()

# Example: Query a user's details by user_id
user_id = "qVc8ODYU5SZjKXVBgXdI7w"  # Replace with the desired user ID
cursor.execute("""
SELECT name, review_count, yelping_since, useful, funny, cool, elite 
FROM user WHERE user_id = ?
""", (user_id,))

# Fetch and display results
results = cursor.fetchone()
if results:
    name, review_count, yelping_since, useful, funny, cool, elite = results
    print(f"User ID: {user_id}\nName: {name}\nReviews Written: {review_count}\nYelping Since: {yelping_since}")
    print(f"Useful: {useful}, Funny: {funny}, Cool: {cool}\nElite: {elite}")
else:
    print(f"No user found with ID '{user_id}'.")

# Example: Find the top 5 users with the highest review counts
cursor.execute("""
SELECT user_id, name, review_count 
FROM user 
ORDER BY review_count DESC 
LIMIT 5
""")
results = cursor.fetchall()
print("\nTop 5 users with the highest review counts:")
for user_id, name, review_count in results:
    print(f"User ID: {user_id}, Name: {name}, Review Count: {review_count}")

# Example: List all elite users
cursor.execute("SELECT user_id, name, elite FROM user WHERE elite IS NOT NULL")
results = cursor.fetchall()
print("\nElite Users:")
for user_id, name, elite in results:
    print(f"User ID: {user_id}, Name: {name}, Elite Year: {elite}")

# Close connection
conn.close()