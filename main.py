from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TOKEN
from keyboards import menu

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    text = """
🎨 Assalomu alaykum va NovaDesign botiga xush kelibsiz!

Quyidagi menyudan kerakli bo'limni tanlang.
"""

    await message.answer(text, reply_markup=menu)


@dp.message(F.text == "📋 Xizmatlar")
async def services(message: Message):
    await message.answer(
        """📋 Xizmatlarimiz:

• Logo dizayn
• Instagram post
• Story dizayn
• Telegram banner
• YouTube Thumbnail
• Avatar
• Branding
• Dasturiy yechimlar"""
    )


@dp.message(F.text == "💰 Narxlar")
async def prices(message: Message):
    await message.answer(
        """💰 Narxlar

Oddiy dizayn:
100 000 so'mdan

Premium dizayn:
1 000 000 so'mgacha"""
    )


@dp.message(F.text == "🖼 Portfolio")
async def portfolio(message: Message):
    await message.answer(
        "Portfolio kanalimiz:\nhttps://t.me/NovaDesign_uzb"
    )


@dp.message(F.text == "📞 Aloqa")
async def contact(message: Message):
    await message.answer(
        "Admin:\n@NovaDesign_uz"
    )
