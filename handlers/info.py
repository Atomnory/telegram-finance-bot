from loader import dp
from aiogram.types import Message
from services.service import get_formatted_categories, get_formatted_types


@dp.message_handler(commands=['categories'])
async def categories_list(message: Message):
    answer_message = get_formatted_categories()
    await message.answer(answer_message)


@dp.message_handler(commands=['types'])
async def types_list(message: Message):
    answer_message = get_formatted_types()
    await message.answer(answer_message)
