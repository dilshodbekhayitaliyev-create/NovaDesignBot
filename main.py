import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Buyurtma berish")],
        [
            KeyboardButton(text="🎨 Xizmatlar"),
            KeyboardButton(text="💰 Narxlar")
        ],
        [
            KeyboardButton(text="🖼 Portfolio"),
            KeyboardButton(text="☎️ Aloqa")
        ],
        [KeyboardButton(text="🤖 AI yordamchi")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "🎨 <b>Assalomu alaykum va NovaDesign'ga xush kelibsiz!</b>\n\n"
        "Biz siz uchun professional grafik dizayn xizmatlarini taqdim etamiz.\n\n"
        "Quyidagi menyudan foydalaning."
    )

    await message.answer(
        text,
        reply_markup=menu,
        parse_mode="HTML"
    )


@dp.message(F.text == "🎨 Xizmatlar")
async def services(message: Message):
    await message.answer(
        "📌 Xizmatlar:\n\n"
        "• Logo dizayn\n"
        "• Instagram post\n"
        "• Story dizayn\n"
        "• Telegram banner\n"
        "• YouTube thumbnail\n"
        "• Branding\n"
        "• Dasturiy yechimlar"
    )


@dp.message(F.text == "💰 Narxlar")
async def prices(message: Message):
    await message.answer(
        "💰 Narxlar:\n\n"
        "Oddiy dizayn — 50 000 so'mdan\n"
        "Premium dizayn — 1 000 000 so'mgacha"
    )


@dp.message(F.text == "☎️ Aloqa")
async def contact(message: Message):
    await message.answer(
        "📩 Admin: @NovaDesign_uz"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
