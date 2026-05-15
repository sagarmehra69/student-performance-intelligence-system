import os
import sqlite3
import hashlib


# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "..", "spis.db")


# =====================================================
# DATABASE CONNECTION
# =====================================================

def connect_db():

    conn = sqlite3.connect(DB_PATH)

    return conn


# =====================================================
# CREATE USERS TABLE
# =====================================================

def create_users_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()


# =====================================================
# HASH PASSWORD
# =====================================================

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


# =====================================================
# ADD USER
# =====================================================

def add_user(username, password, role):

    conn = connect_db()

    cursor = conn.cursor()

    hashed = hash_password(password)

    try:

        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            """,
            (username, hashed, role)
        )

        conn.commit()

    except Exception as e:

        print("Database Error:", e)

    conn.close()


# =====================================================
# REGISTER USER
# =====================================================

def register_user(username, password, role):

    conn = connect_db()

    cursor = conn.cursor()

    hashed = hash_password(password)

    try:

        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            """,
            (username, hashed, role)
        )

        conn.commit()

        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False
# =====================================================
# LOGIN USER
# =====================================================

def login_user(username, password):

    conn = connect_db()

    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (username, hashed)
    )

    data = cursor.fetchone()

    conn.close()

    return data


# =====================================================
# INITIALIZE DATABASE
# =====================================================

create_users_table()

# Default Users
add_user("admin", "admin123", "Admin")
add_user("student", "student123", "Student")