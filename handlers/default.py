from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(commands=['wow'])
async def reply_keyboard_test(message: Message):
    key = [['1 uno', '2 uno', '3 uno'],
           [KeyboardButton('/start'), KeyboardButton('/categories'), KeyboardButton('/expenses')],
           [KeyboardButton('/start'), '/start', KeyboardButton('/wow'), '/wow']]
    keyboard = ReplyKeyboardMarkup(keyboard=key, one_time_keyboard=True)

    rep = ReplyKeyboardMarkup()
    rep.row()
    rep.insert(KeyboardButton('ins1'))
    rep.insert(KeyboardButton('ins2'))
    rep.row()
    rep.add(KeyboardButton('add1'), KeyboardButton('add2'), KeyboardButton('add3'))
    rep.row(KeyboardButton('row1'), KeyboardButton('row2'), KeyboardButton('row3'), KeyboardButton('row4'))
    rep.insert('insert text')
    rep.row(KeyboardButton('row1'), KeyboardButton('row2'), KeyboardButton('row3'))
    rep.add(KeyboardButton('add1'), KeyboardButton('add2'), KeyboardButton('add3'))
    rep.insert(KeyboardButton('ins1'))
    rep.insert(KeyboardButton('ins2'))
    rep.add(KeyboardButton('add1'), KeyboardButton('add2'), KeyboardButton('add3'))
    rep.insert(KeyboardButton('ins3'))
    rep.insert((KeyboardButton('ins4')))

    await message.answer('!', reply_markup=rep)


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
