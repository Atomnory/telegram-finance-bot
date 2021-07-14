from loader import dp
from aiogram.types import Message
from services.statistics.yearstatistic import YearStatistic


@dp.message_handler(commands=['year'])
async def year_statistic(message: Message):
    answer_message = YearStatistic().get_sum()
    await message.answer(answer_message)


@dp.message_handler(commands=['year_category'])
async def year_statistic_by_category(message: Message):
    answer_message = YearStatistic().get_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['year_type'])
async def year_statistic_by_type(message: Message):
    answer_message = YearStatistic().get_by_type()
    await message.answer(answer_message)
