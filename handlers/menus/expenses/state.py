from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateExpense(StatesGroup):
    waiting_for_start = State()
    waiting_for_type = State()
    waiting_for_category = State()
    waiting_for_payment_type = State()
    waiting_for_additional_info = State()
    waiting_for_amount = State()
    waiting_for_confirm = State()
