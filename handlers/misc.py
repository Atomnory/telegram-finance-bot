from loader import dp
from aiogram.types import Message
from utils import exceptions
from services import expense


@dp.message_handler(lambda message: message.text.startswith('/delete'))
async def delete_expense(message: Message):
    """ Delete expense row with id. """
    row_id = int(message.text[7:])
    expense.delete_expense(row_id)
    answer_message = 'Expense was deleted.'
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def last_expenses(message: Message):
    """ Display last expense (10 by default). """
    answer_message = expense.last_expenses()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense_by_message(message: Message):
    try:
        answer_message = expense.add_expense(message.text)
    except exceptions.NotCorrectMessage \
        or exceptions.CategoryDoesNotExist \
        or exceptions.TypeOfCategoryDoesNotExist \
            as e:
        await message.answer(str(e))
        return
    await message.answer(answer_message)
