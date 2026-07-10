import sqlite3

db = sqlite3.connect("bot.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    username TEXT
)
""")

db.commit()
# database.py faylingiz oxiriga qo'shing:

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
