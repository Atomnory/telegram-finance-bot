from aiogram import executor
from loader import dp
import handlers

# TODO: create handler funcs to adding expense with keyboard only
# TODO: change all navigation to keyboard

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
