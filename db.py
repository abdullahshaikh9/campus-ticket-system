import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "campus.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending',
        FOREIGN KEY (student_id) REFERENCES users(user_id)
    );
    """)
    # Seed data
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                    ("student1", generate_password_hash("pass123"), "student"))
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                    ("admin", generate_password_hash("admin123"), "admin"))
        cur.execute("INSERT INTO tickets (student_id, title, category) VALUES (?, ?, ?)", 
                    (1, "Wi-Fi not working in Lab 3", "IT"))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None

def create_ticket(student_id, title, category):
    conn = get_db()
    conn.execute("INSERT INTO tickets (student_id, title, category) VALUES (?, ?, ?)", 
                 (student_id, title, category))
    conn.commit()
    conn.close()

def get_student_tickets(student_id):
    conn = get_db()
    tickets = conn.execute("SELECT * FROM tickets WHERE student_id = ? ORDER BY ticket_id DESC", (student_id,)).fetchall()
    conn.close()
    return tickets

def get_all_tickets():
    conn = get_db()
    tickets = conn.execute("SELECT tickets.*, users.username FROM tickets JOIN users ON tickets.student_id = users.user_id ORDER BY ticket_id DESC").fetchall()
    conn.close()
    return tickets

def update_ticket_status(ticket_id, new_status):
    conn = get_db()
    ticket = conn.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    
    if not ticket:
        return False, "Ticket not found"
        
    # NFR2: Enforce Workflow (Cannot jump from Pending directly to Resolved)
    if ticket["status"] == "Pending" and new_status == "Resolved":
        return False, "Error: Must mark as 'In Progress' first."
        
    conn.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()
    return True, "Status updated successfully"