from loader import dp
from aiogram.types import Message
from services import expense


@dp.message_handler(lambda message: message.text.startswith('/delete'))
async def delete_expense(message: Message):
    """ Delete expense row with id. """
    row_id = int(message.text[7:])
    answer_message = expense.ExpenseDeleter().delete_expense(row_id)
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def last_expenses(message: Message):
    """ Display last expense. """
    answer_message = expense.ExpenseDisplayer().get_last()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense_by_message(message: Message):
    try:
        answer_message = expense.ExpenseCreator().parse_message_and_create_expense_if_valid(message.text)
    except Exception as e:
        print(e)
        await message.answer('Error: ' + str(e))
        return
    await message.answer(answer_message)
