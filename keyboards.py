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
