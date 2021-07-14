from loader import dp
from aiogram.types import Message
from services.statistics.monthstatistic import MonthStatistic


@dp.message_handler(commands=['month'])
async def month_statistic(message: Message):
    answer_message = MonthStatistic().get_sum()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_category'])
async def month_statistic_by_category(message: Message):
    answer_message = MonthStatistic().get_by_category()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_type'])
async def month_statistic_by_type(message: Message):
    answer_message = MonthStatistic().get_by_type()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_detail'])
async def month_statistic_detail(message: Message):
    answer_message = MonthStatistic().get_with_detail()
    await message.answer(answer_message)
