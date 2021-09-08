import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.middleware import AccessMiddleware
from utils import config
from db_table import inspect_db

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()       # opportunity change MemoryStorage to Redis
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AccessMiddleware(config.ACCESS_USER_ID))
inspect_db()
