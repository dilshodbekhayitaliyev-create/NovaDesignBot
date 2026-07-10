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
# main.py faylingizga kerakli importlar va handlerlarni qo'shing:

from aiogram.types import CallbackQuery
from states import PaymentState # states.py faylingizga class PaymentState(StatesGroup): screenshot = State() deb qo'shing
import keyboards as kb
import database as db

# --- ADMIN PANEL KIRISH ---
@dp.message(F.text == "/admin")
async def admin_panel_start(message: Message):
    if message.from_user.id in config.ADMINS:
        await message.answer("NovaDesign CRM tizimiga xush kelibsiz, Admin!", reply_markup=kb.admin_panel_menu())
    else:
        await message.answer("Siz admin emassiz!")

@dp.message(F.text == "📊 Statistika")
async def show_bot_stats(message: Message):
    if message.from_user.id in config.ADMINS:
        users, all_orders, done, canceled = db.get_stats()
        text = (f"📊 **NovaDesign Bot Statistikasi:**\n\n"
                f"👥 Jami foydalanuvchilar: {users} ta\n"
                f"📦 Jami buyurtmalar: {all_orders} ta\n"
                f"✅ Yakunlangan: {done} ta\n"
                f"❌ Bekor qilingan: {canceled} ta")
        await message.answer(text)

# --- MIJOZ: TO'LOV CHEKINI YUBORISH ---
@dp.message(F.text == "💳 To’lov")
async def start_payment(message: Message, state: FSMContext):
    await message.answer(
        f"To'lov uchun Humo karta raqami:\n`{config.KARTA_RAQAM}`\n\n"
        f"⚠️ To'lovni amalga oshirgach, **chek skrinshotini (rasm formatida)** shu yerga yuboring:",
        parse_mode="Markdown"
    )
    await state.set_state(PaymentState.screenshot)

@dp.message(PaymentState.screenshot, F.photo)
async def process_payment_screenshot(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.clear()
    await message.answer("Rahmat! Chek qabul qilindi, admin tasdiqlashini kuting. 🎉")
    
    # Adminga chekni tekshirish uchun yuborish
    for admin in config.ADMINS:
        try:
            await bot.send_photo(
                chat_id=admin,
                photo=photo_id,
                caption=f"💳 **Yangi to'lov cheki keldi!**\nKimdan: @{message.from_user.username or 'Yashirin'}\nID: {message.from_user.id}",
                reply_markup=kb.admin_payment_buttons(message.from_user.id) # Callback uchun ID yuboramiz
            )
        except Exception as e:
            print(f"Adminga chek yuborishda xato: {e}")

# --- ADMIN: BUYURTMA STATUSLARINI BOSHQARISH (CALLBACKS) ---
@dp.callback_query(F.data.startswith("status_"))
async def handle_order_status(call: CallbackQuery):
    # status_process_1, status_ready_1 kabi ma'lumotlarni ajratib olamiz
    data = call.data.split("_")
    action = data[1]  # process, ready, cancel
    order_id = int(data[2])
    
    order = db.get_order_by_id(order_id)
    if not order:
        await call.answer("Buyurtma topilmadi!", show_alert=True)
        return
        
    client_id, name, phone, service, desc, current_status = order
    
    if action == "process":
        db.update_order_status(order_id, "Jarayonda")
        await call.message.edit_text(f"📦 **Buyurtma #{order_id} holati o'zgardi:**\nHolat: ⏳ Jarayonda")
        await bot.send_message(client_id, f"🚀 **NovaDesign:** Sizning #{order_id} sonli buyurtmangiz dizaynerlarimiz tomonidan jarayonga qabul qilindi!")
        
    elif action == "ready":
        db.update_order_status(order_id, "Tayyor")
        await call.message.edit_text(f"📦 **Buyurtma #{order_id} holati o'zgardi:**\nHolat: ✅ Tayyor")
        await bot.send_message(client_id, f"🎉 **NovaDesign:** Ura! Sizning #{order_id} sonli buyurtmangiz muvaffaqiyatli tayyor bo'ldi. Admin tez orada fayllarni yuboradi.")
        
    elif action == "cancel":
        db.update_order_status(order_id, "Bekor qilingan")
        await call.message.edit_text(f"📦 **Buyurtma #{order_id} holati o'zgardi:**\nHolat: ❌ Bekor qilingan")
        await bot.send_message(client_id, f"❌ **NovaDesign:** Sizning #{order_id} sonli buyurtmangiz bekor qilindi. Batafsil ma'lumot uchun admin bilan bog'laning.")
        
    await call.answer("Holat yangilandi!")

# --- ADMIN: TO'LOVNI TASDIQLASH ---
@dp.callback_query(F.data.startswith("pay_"))
async def handle_payment_status(call: CallbackQuery):
    data = call.data.split("_")
    action = data[1] # confirm, reject
    client_id = int(data[2])
    
    if action == "confirm":
        await call.message.edit_caption(caption=call.message.caption + "\n\n✅ **To'lov tasdiqlandi!**")
        await bot.send_message(client_id, "✅ **NovaDesign:** To'lovingiz muvaffaqiyatli qabul qilindi va tasdiqlandi! Rahmat.")
    elif action == "reject":
        await call.message.edit_caption(caption=call.message.caption + "\n\n❌ **To'lov rad etildi!**")
        await bot.send_message(client_id, "❌ **NovaDesign:** Afsuski, yuborgan chekingiz tasdiqlanmadi. Iltimos, qaytadan tekshirib yuboring yoki admin bilan bog'laning.")
        
    await call.answer()
