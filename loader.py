import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from services.middleware import AccessMiddleware
from services import config


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AccessMiddleware(config.ACCESS_USER_ID))
