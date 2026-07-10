from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    name = State()         # Ism olish
    phone = State()        # Telefon raqam olish
    service = State()      # Xizmat turini tanlash
    description = State()  # Buyurtma tavsifini olish

class PaymentState(StatesGroup):
    screenshot = State()   # To'lov chekini olish
