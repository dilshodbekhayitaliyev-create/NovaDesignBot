from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Bosh menyu
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Buyurtma berish")],
        [KeyboardButton(text="📋 Xizmatlar"), KeyboardButton(text="💰 Narxlar")],
        [KeyboardButton(text="🖼 Portfolio"), KeyboardButton(text="💳 To'lov")],
        [KeyboardButton(text="📞 Aloqa")]
    ],
    resize_keyboard=True
)

# Xizmatlar ro'yxati menyusi (Mijoz buyurtma berayotganda tanlashi uchun)
def services_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Logo dizayn"), KeyboardButton(text="Instagram post & story")],
            [KeyboardButton(text="Telegram banner & preview"), KeyboardButton(text="YouTube thumbnail")],
            [KeyboardButton(text="Avatar"), KeyboardButton(text="Branding")],
            [KeyboardButton(text="Dasturiy yechimlar")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )

# Telefon raqamini yuborish tugmasi
def share_phone_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )

# Admin uchun buyurtmani boshqarish tugmalari
def admin_order_buttons(order_id):
    """Admin uchun buyurtmani boshqarish tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏳ Jarayonda", callback_data=f"status_process_{order_id}"),
                InlineKeyboardButton(text="✅ Tayyor", callback_data=f"status_ready_{order_id}")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"status_cancel_{order_id}")
            ]
        ]
    )

# Admin chekni tasdiqlashi uchun tugmalar
def admin_payment_buttons(order_id):
    """Admin chekni tasdiqlashi uchun tugmalar"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 To'lovni tasdiqlash", callback_data=f"pay_confirm_{order_id}"),
                InlineKeyboardButton(text="👎 To'lov rad etildi", callback_data=f"pay_reject_{order_id}")
            ]
        ]
    )

# /admin buyrug'i bosilganda chiquvchi menyu
def admin_panel_menu():
    """/admin buyrug'i bosilganda chiquvchi menyu"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Reklama yuborish")],
            [KeyboardButton(text="⬅️ Bosh menyu")]
        ],
        resize_keyboard=True
    )
