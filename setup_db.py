import sqlite3

def initialize_database():
    # Connect to database
    conn = sqlite3.connect("C:\\Users\\HP\\Downloads\\project\\Webcam_Spyware_Security\\database.db")
    cursor = conn.cursor()

    # Create 'users' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            face_data BLOB
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("✅ Database initialized successfully!")
