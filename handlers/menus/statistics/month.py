from loader import dp
from aiogram.types import Message
from statistic import get_month_sum_statistic, get_month_statistic_by_category
from statistic import get_month_statistic_by_type, get_detail_month_statistic


@dp.message_handler(commands=['month'])
async def month_statistic(message: Message):
    answer_message = get_month_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_category'])
async def month_statistic_by_category(message: Message):
    answer_message = get_month_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_type'])
async def month_statistic_by_type(message: Message):
    answer_message = get_month_statistic_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_detail'])
async def month_statistic_detail(message: Message):
    answer_message = get_detail_month_statistic()
    await message.answer(answer_message)
