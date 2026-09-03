import sqlite3
import bcrypt

DB_NAME = "app_database.db"

def init_db():
    """Membuat tabel users, documents, dan chats jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabel User
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Tabel Dokumen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            summary TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabel Riwayat Chat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- AUTENTIKASI USER ---
def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "Registrasi berhasil! Silakan login."
    except sqlite3.IntegrityError:
        return False, "Username sudah digunakan."
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return user[0]  # Mengembalikan user_id
    return None

# --- MANAGEMENT RIWAYAT ---
def save_document(user_id, filename, summary=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (user_id, filename, summary) VALUES (?, ?, ?)", (user_id, filename, summary))
    conn.commit()
    doc_id = cursor.lastrowid
    conn.close()
    return doc_id

def update_summary(doc_id, summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE documents SET summary = ? WHERE id = ?", (summary, doc_id))
    conn.commit()
    conn.close()

def save_chat_message(doc_id, role, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (doc_id, role, message) VALUES (?, ?, ?)", (doc_id, role, message))
    conn.commit()
    conn.close()

def get_user_documents(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, summary FROM documents WHERE user_id = ? ORDER BY id DESC", (user_id,))
    docs = cursor.fetchall()
    conn.close()
    return docs

def get_chat_history(doc_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role, message FROM chats WHERE doc_id = ? ORDER BY id ASC", (doc_id,))
    chats = cursor.fetchall()
    conn.close()
    return chats