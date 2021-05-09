import os
import logging

from aiogram import Bot, Dispatcher, executor, types

from middleware import AccessMiddleware
import expense
from category import Categories
import exceptions

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
    await message.answer("Hola\nI'm Bot\nPowered by aiogram")


@dp.message_handler(lambda message: message.text.startswith('/delete'))
async def delete_expense(message: types.Message):
    """ Delete expense row with id"""
    row_id = int(message.text[7:])
    expense.delete_expense(row_id)
    answer_message = 'Expense was deleted.'
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def last_expenses(message: types.Message):
    last_ten = expense.last_ten()
    if not last_ten:
        await message.answer("There's none any expense")
        return

    last_ten_rows = [
        f"{expense_obj.amount} \u20BD "
        f"for '{expense_obj.get_category_name()}' category. "
        f"Click /delete{expense_obj.id} to delete it."
        for expense_obj in last_ten
    ]
    answer_message = "Last expenses: \n\n* " + "\n\n* ".join(last_ten_rows)
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
                     f"to '{new_expense.get_category_name()}' category. \n\n " \
                     f"To see all expenses: /expenses"
    await message.answer(answer_message)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



