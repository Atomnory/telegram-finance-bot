import logging
from aiogram import Bot, Dispatcher
from services.middleware import AccessMiddleware
from services import config


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(config.ACCESS_USER_ID))
