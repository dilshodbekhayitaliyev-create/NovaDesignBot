import sqlite3

def init_db():
    """Baza va jadvallarni yaratish"""
    conn = sqlite3.connect("novadesign.db")
    cursor = conn.cursor()
    
    # Foydalanuvchilar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        username TEXT
    )
    """)
    
    # Buyurtmalar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        phone TEXT,
        service TEXT,
        description TEXT,
        status TEXT DEFAULT 'Kutilmoqda'
    )
    """)
    
    conn.commit()
    conn.close()

def add_user(user_id, full_name, username):
    """Yangi foydalanuvchini bazaga qo'shish"""
    conn = sqlite3.connect("novadesign.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)", (user_id, full_name, username))
    conn.commit()
    conn.close()

def add_order(user_id, name, phone, service, description):
    """Yangi buyurtmani bazaga saqlash"""
    conn = sqlite3.connect("novadesign.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, name, phone, service, description) VALUES (?, ?, ?, ?, ?)",
                   (user_id, name, phone, service, description))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def update_order_status(order_id, new_status):
    """Buyurtma holatini yangilash (Jarayonda, Tayyor, Bekor qilingan)"""
    conn = sqlite3.connect('novadesign.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

def get_order_by_id(order_id):
    """Buyurtma ma'lumotlarini ID bo'yicha olish"""
    conn = sqlite3.connect('novadesign.db')
    cursor = conn.cursor()
    order = cursor.execute("SELECT user_id, name, phone, service, description, status FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    return order

def get_all_users():
    """Reklama yuborish uchun barcha foydalanuvchilar ID'sini olish"""
    conn = sqlite3.connect('novadesign.db')
    cursor = conn.cursor()
    users = cursor.execute("SELECT user_id FROM users").fetchall()
    conn.close()
    return [u[0] for u in users]

def get_stats():
    """Statistikani hisoblash funksiyasi"""
    conn = sqlite3.connect('novadesign.db')
    cursor = conn.cursor()
    users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    all_orders = cursor.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    done = cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Tayyor'").fetchone()[0]
    canceled = cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Bekor qilingan'").fetchone()[0]
    conn.close()
    return users, all_orders, done, canceled
