from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    """ This handler will be called when user sends '/start' or '/help' command. """
    answer_message = ("What do yo want to do?\n"
                      "Add expenses with 'Add'")
    start_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('/categories'),
                KeyboardButton('/types')
            ],
            [
                KeyboardButton('/expenses'),
                KeyboardButton('/day'),
                KeyboardButton('Add')
            ]
        ],
        one_time_keyboard=True
    )
    await message.answer(answer_message, reply_markup=start_menu)
