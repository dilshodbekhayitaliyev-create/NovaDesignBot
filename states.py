from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    ism = State()
    telefon = State()
    xizmat = State()
    izoh = State()
