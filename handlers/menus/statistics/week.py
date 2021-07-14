from loader import dp
from aiogram.types import Message
from services.statistics.weekstatistic import WeekStatistic


@dp.message_handler(commands=['week'])
async def week_statistic(message: Message):
    answer_message = WeekStatistic().get_sum()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_category'])
async def week_statistic_by_category(message: Message):
    answer_message = WeekStatistic().get_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_type'])
async def week_statistic_by_type(message: Message):
    answer_message = WeekStatistic().get_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['week_detail'])
async def week_statistic_detail(message: Message):
    answer_message = WeekStatistic().get_with_detail()
    await message.answer(answer_message)
