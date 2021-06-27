from loader import dp
from aiogram.types import Message
from services.statistic import get_week_sum_statistic, get_week_statistic_by_category
from services.statistic import get_week_statistic_by_type, get_detail_week_statistic


@dp.message_handler(commands=['week'])
async def week_statistic(message: Message):
    answer_message = get_week_sum_statistic()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_category'])
async def week_statistic_by_category(message: Message):
    answer_message = get_week_statistic_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_type'])
async def week_statistic_by_type(message: Message):
    answer_message = get_week_statistic_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_detail'])
async def week_statistic_detail(message: Message):
    answer_message = get_detail_week_statistic()
    await message.answer(answer_message)
