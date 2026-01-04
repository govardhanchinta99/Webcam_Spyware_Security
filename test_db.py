import sqlite3

# Sample data
username = "test_user"
password = "test123"
face_blob = b"sample_face_data_as_bytes"  # In real case, this would be actual image bytes

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Check if 'users' table exists (optional safety check)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if cursor.fetchone() is None:
    print("❌ 'users' table does not exist. Run setup_db.py first.")
else:
    try:
        # Insert a sample user
        cursor.execute("INSERT INTO users (username, password, face_data) VALUES (?, ?, ?)",
                       (username, password, face_blob))
        conn.commit()
        print("✅ Sample user inserted into the database.")
    except sqlite3.IntegrityError:
        print("⚠️ User already exists.")

    # Retrieve all users to confirm
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    print("📋 Users in database:")
    for user in users:
        print(f" - ID: {user[0]}, Username: {user[1]}")

conn.close()
