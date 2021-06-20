from loader import dp
from aiogram.types import Message
from statistic import get_today_sum_statistic, get_today_statistic_by_category, get_today_statistic_by_type


@dp.message_handler(commands=['day'])
async def today_statistic(message: Message):
    answer_message = get_today_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['day_category'])
async def today_statistic_by_category(message: Message):
    answer_message = get_today_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['day_type'])
async def today_statistic_by_type(message: Message):
    answer_message = get_today_statistic_by_type()
    await message.answer(answer_message)
