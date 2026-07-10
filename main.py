import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# Fayllarimizdan import qilamiz
import config
import database as db
import keyboards as kb
from states import OrderState, PaymentState

bot = Bot(config.TOKEN)
dp = Dispatcher()

# --- START BUYRUG'I ---
@dp.message(CommandStart())
async def start(message: Message):
    # Foydalanuvchini bazaga qo'shish
    db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    text = "🎨 Assalomu alaykum va NovaDesign botiga xush kelibsiz!\n\nQuyidagi menyudan kerakli bo'limni tanlang."
    await message.answer(text, reply_markup=kb.menu)

# --- BILDIRISHNOMALAR VA INFO ---
@dp.message(F.text == "📋 Xizmatlar")
async def services(message: Message):
    await message.answer(
        "📋 Xizmatlarimiz:\n\n• Logo dizayn\n• Instagram post\n• Story dizayn\n• Telegram banner\n• YouTube Thumbnail\n• Avatar\n• Branding\n• Dasturiy yechimlar"
    )

@dp.message(F.text == "💰 Narxlar")
async def prices(message: Message):
    await message.answer(
        "💰 Narxlar\n\nOddiy dizayn:\n100 000 so'mdan\n\nPremium dizayn:\n1 000 000 so'mgacha"
    )

@dp.message(F.text == "🖼 Portfolio")
async def portfolio(message: Message):
    await message.answer("Portfolio kanalimiz:\nhttps://t.me/NovaDesign_uzb")

@dp.message(F.text == "📞 Aloqa")
async def contact(message: Message):
    await message.answer("Admin:\n@NovaDesign_uz")

# --- MULTI-MENU ORQAGA / BEKOR QILISH ---
@dp.message(F.text == "❌ Bekor qilish")
@dp.message(F.text == "⬅️ Bosh menyu")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh menyuga qaytdingiz.", reply_markup=kb.menu)

# --- MIJOZ: BUYURTMA BERISH BOSQICHLARI (FSM) ---
@dp.message(F.text == "🛍 Buyurtma berish")
async def start_order(message: Message, state: FSMContext):
    await state.set_state(OrderState.name)
    await message.answer("Iltimos, ismingizni kiriting:", reply_markup=kb.ReplyKeyboardMarkup(keyboard=[[kb.KeyboardButton(text="❌ Bekor qilish")]], resize_keyboard=True))

@dp.message(OrderState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderState.phone)
    await message.answer("Telefon raqamingizni kiriting yoki quyidagi tugmani bosing:", reply_markup=kb.share_phone_menu())

@dp.message(OrderState.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    await state.set_state(OrderState.service)
    await message.answer("Kerakli xizmat turini tanlang:", reply_markup=kb.services_menu())

@dp.message(OrderState.service)
async def process_service(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(OrderState.description)
    await message.answer("Buyurtma tavsifini yozing (batafsil ma'lumot bering):")

@dp.message(OrderState.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    
    # Bazaga saqlash
    order_id = db.add_order(message.from_user.id, data['name'], data['phone'], data['service'], data['description'])
    
    # Admin matni
    admin_text = (f"🔔 **Yangi Buyurtma #{order_id}**\n\n"
                  f"👤 Mijoz: {data['name']}\n"
                  f"📞 Tel: {data['phone']}\n"
                  f"💼 Xizmat: {data['service']}\n"
                  f"📝 Tavsif: {data['description']}")
    
    for admin in config.ADMINS:
        try:
            await bot.send_message(chat_id=admin, text=admin_text, reply_markup=kb.admin_order_buttons(order_id))
        except Exception as e:
            print(f"Adminga yuborishda xato: {e}")

    await message.answer("Rahmat! Buyurtmangiz qabul qilindi va adminlarga yuborildi. Yaqin orada siz bilan bog'lanamiz.", reply_markup=kb.menu)
    await state.clear()

# --- MIJOZ: TO'LOV CHEKINI YUBORISH ---
@dp.message(F.text == "💳 To'lov")
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
    await message.answer("Rahmat! Chek qabul qilindi, admin tasdiqlashini kuting. 🎉", reply_markup=kb.menu)
    
    for admin in config.ADMINS:
        try:
            await bot.send_photo(
                chat_id=admin,
                photo=photo_id,
                caption=f"💳 **Yangi to'lov cheki keldi!**\nKimdan: @{message.from_user.username or 'Yashirin'}\nID: {message.from_user.id}",
                reply_markup=kb.admin_payment_buttons(message.from_user.id)
            )
        except Exception as e:
            print(f"Adminga chek yuborishda xato: {e}")

# --- ADMIN PANEL ---
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

# --- ADMIN: STATUS CALLBACKS ---
@dp.callback_query(F.data.startswith("status_"))
async def handle_order_status(call: CallbackQuery):
    data = call.data.split("_")
    action, order_id = data[1], int(data[2])
    order = db.get_order_by_id(order_id)
    
    if not order:
        await call.answer("Buyurtma topilmadi!", show_alert=True)
        return
        
    client_id, name, phone, service, desc, current_status = order
    
    if action == "process":
        db.update_order_status(order_id, "Jarayonda")
        await call.message.edit_text(f"📦 **Buyurtma #{order_id} holati o'zgardi:**\nHolat: ⏳ Jarayonda")
        await bot.send_message(client_id, f"🚀 **NovaDesign:** Sizning #{order_id} sonli buyurtmangiz jarayonga qabul qilindi!")
    elif action == "ready":
        db.update_order_status(order_id, "Tayyor")
        await call.message.edit_text(f"📦 **Buyurtma #{order_id} holati o'zgardi:**\nHolat: ✅ Tayyor")
        await bot.send_message(client_id, f"🎉 **NovaDesign:** Ura! Sizning #{order_id} sonli buyurtmangiz tayyor bo'ldi!")
    elif action == "cancel":
        db.update_order_status(order_id, "Bekor qilingan")
        await call.message.edit_text(f"📦 **Buyurtma #{order_id} holati o'zgardi:**\nHolat: ❌ Bekor qilingan")
        await bot.send_message(client_id, f"❌ **NovaDesign:** Sizning #{order_id} sonli buyurtmangiz bekor qilindi.")
        
    await call.answer("Holat yangilandi!")

# --- ADMIN: TO'LOV CALLBACKS ---
@dp.callback_query(F.data.startswith("pay_"))
async def handle_payment_status(call: CallbackQuery):
    data = call.data.split("_")
    action, client_id = data[1], int(data[2])
    
    if action == "confirm":
        await call.message.edit_caption(caption=call.message.caption + "\n\n✅ **To'lov tasdiqlandi!**")
        await bot.send_message(client_id, "✅ **NovaDesign:** To'lovingiz muvaffaqiyatli qabul qilindi va tasdiqlandi!")
    elif action == "reject":
        await call.message.edit_caption(caption=call.message.caption + "\n\n❌ **To'lov rad etildi!**")
        await bot.send_message(client_id, "❌ **NovaDesign:** Afsuski, yuborgan chekingiz tasdiqlanmadi.")
        
    await call.answer()

# --- ISHGA TUSHIRISH ---
async def main():
    db.init_db()  # Bazani tekshirish/yaratish
    print("NovaDesign Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
