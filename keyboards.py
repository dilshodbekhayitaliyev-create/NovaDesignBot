from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Buyurtma berish")],
        [KeyboardButton(text="📋 Xizmatlar"), KeyboardButton(text="💰 Narxlar")],
        [KeyboardButton(text="🖼 Portfolio"), KeyboardButton(text="💳 To'lov")],
        [KeyboardButton(text="📞 Aloqa")]
    ],
    resize_keyboard=True
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

def admin_panel_menu():
    """/admin buyrug'i bosilganda chiquvchi menyu"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Reklama yuborish")],
            [KeyboardButton(text="⬅️ Bosh menyu")]
        ],
        resize_keyboard=True
    )
