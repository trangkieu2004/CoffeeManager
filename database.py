import sqlite3, hashlib

DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL,
            permissions TEXT
        )
    """)
    # tạo admin mặc định
    cursor.execute("SELECT * FROM users WHERE role='admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username,password,role) VALUES (?, ?, ?)",
                       ("admin", hashlib.sha256("admin123".encode()).hexdigest(), "admin"))
    conn.commit()
    conn.close()

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
