import logging
from middleware import AccessMiddleware

from aiogram import Bot, Dispatcher, executor, types
from services import config, exceptions, service
import expense
import statistic
# TODO: create handler funcs to adding expense with keyboard only
# TODO: change all navigation to keyboard

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(config.ACCESS_USER_ID))


# @dp.message_handler(commands=['wow'])
# async def reply_keyboard_test(message: types.Message):
#     key = [['1 uno', '2 uno', '3 uno'],
#            [types.KeyboardButton('/start'), types.KeyboardButton('/categories'), types.KeyboardButton('/expenses')],
#            [types.KeyboardButton('/start'), '/start', types.KeyboardButton('/wow'), '/wow']]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=key, one_time_keyboard=True)
#
#     rep = types.ReplyKeyboardMarkup()
#     rep.row()
#     rep.insert(types.KeyboardButton('ins1'))
#     rep.insert(types.KeyboardButton('ins2'))
#     rep.row()
#     rep.add(types.KeyboardButton('add1'), types.KeyboardButton('add2'), types.KeyboardButton('add3'))
#     rep.row(types.KeyboardButton('row1'), types.KeyboardButton('row2'), types.KeyboardButton('row3'), types.KeyboardButton('row4'))
#     rep.insert('insert text')
#     rep.row(types.KeyboardButton('row1'), types.KeyboardButton('row2'), types.KeyboardButton('row3'))
#     rep.add(types.KeyboardButton('add1'), types.KeyboardButton('add2'), types.KeyboardButton('add3'))
#     rep.insert(types.KeyboardButton('ins1'))
#     rep.insert(types.KeyboardButton('ins2'))
#     rep.add(types.KeyboardButton('add1'), types.KeyboardButton('add2'), types.KeyboardButton('add3'))
#     rep.insert(types.KeyboardButton('ins3'))
#     rep.insert((types.KeyboardButton('ins4')))
#
#     await message.answer('!', reply_markup=rep)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ This handler will be called when user sends '/start' or '/help' command. """
    answer_message = ("What do yo want to do?\n"
                      "Add expenses with /add")
    start_menu = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton('/categories'),
                types.KeyboardButton('/types')
            ],
            [
                types.KeyboardButton('/expenses'),
                types.KeyboardButton('/day'),
                types.KeyboardButton('/add')
            ]
        ],
        one_time_keyboard=True
    )
    await message.answer(answer_message, reply_markup=start_menu)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    answer_message = service.get_all_categories()
    await message.answer(answer_message)


@dp.message_handler(commands=['types'])
async def types_list(message: types.Message):
    answer_message = service.get_all_types()
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/delete'))
async def delete_expense(message: types.Message):
    """ Delete expense row with id. """
    row_id = int(message.text[7:])
    expense.delete_expense(row_id)
    answer_message = 'Expense was deleted.'
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def last_expenses(message: types.Message):
    """ Display last expense (10 by default). """
    answer_message = expense.last_expenses()
    await message.answer(answer_message)


@dp.message_handler(commands=['day'])
async def today_statistic(message: types.Message):
    answer_message = statistic.get_today_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['day_category'])
async def today_statistic_by_category(message: types.Message):
    answer_message = statistic.get_today_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['day_type'])
async def today_statistic_by_type(message: types.Message):
    answer_message = statistic.get_today_statistic_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['week'])
async def week_statistic(message: types.Message):
    answer_message = statistic.get_week_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_category'])
async def week_statistic_by_category(message: types.Message):
    answer_message = statistic.get_week_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_type'])
async def week_statistic_by_type(message: types.Message):
    answer_message = statistic.get_week_statistic_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_detail'])
async def week_statistic_detail(message: types.Message):
    answer_message = statistic.get_detail_week_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistic(message: types.Message):
    answer_message = statistic.get_month_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_category'])
async def month_statistic_by_category(message: types.Message):
    answer_message = statistic.get_month_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_type'])
async def month_statistic_by_type(message: types.Message):
    answer_message = statistic.get_month_statistic_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_detail'])
async def month_statistic_detail(message: types.Message):
    answer_message = statistic.get_detail_month_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['year'])
async def year_statistic(message: types.Message):
    answer_message = statistic.get_year_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['year_category'])
async def year_statistic_by_category(message: types.Message):
    answer_message = statistic.get_year_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['year_type'])
async def year_statistic_by_type(message: types.Message):
    answer_message = statistic.get_year_statistic_by_type()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        answer_message = expense.add_expense(message.text)
    except exceptions.NotCorrectMessage \
        or exceptions.CategoryDoesNotExist \
        or exceptions.TypeOfCategoryDoesNotExist \
            as e:
        await message.answer(str(e))
        return
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
