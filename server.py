import os
import logging

from aiogram import Bot, Dispatcher, executor, types

from middleware import AccessMiddleware
import expense
from expense import get_category_name
import exceptions
from statistic import get_today_sum_statistic, get_week_sum_statistic
from statistic import get_month_sum_statistic, get_year_sum_statistic

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN_PB')
ACCESS_USER_ID = os.getenv('TELEGRAM_ACCESS_USER_ID')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_USER_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
        This handler will be called when user sends '/start' or '/help' command.
    """
    await message.answer("Hola\nI'm Bot\nPowered by aiogram\n"
                         "/day /expenses")


@dp.message_handler(lambda message: message.text.startswith('/delete'))
async def delete_expense(message: types.Message):
    """ Delete expense row with id"""
    row_id = int(message.text[7:])
    expense.delete_expense(row_id)
    answer_message = 'Expense was deleted.'
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def last_expenses(message: types.Message):
    answer_message = expense.last_expenses()
    await message.answer(answer_message)


@dp.message_handler(commands=['day'])
async def today_statistic(message: types.Message):
    answer_message = get_today_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['week'])
async def week_statistic(message: types.Message):
    answer_message = get_week_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistic(message: types.Message):
    answer_message = get_month_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['year'])
async def year_statistic(message: types.Message):
    answer_message = get_year_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        new_expense = expense.add_expense(message.text)
    except exceptions.NotCorrectMessage \
        or exceptions.CategoryDoesNotExist \
        or exceptions.TypeOfCategoryDoesNotExist \
            as e:
        await message.answer(str(e))
        return
    answer_message = f"Expense was added for {new_expense.amount} \u20BD " \
                     f"to '{get_category_name(new_expense.category_id)}' category. \n\n " \
                     f"To see all expenses: /expenses"
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
