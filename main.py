from aiogram import executor
from loader import *
import handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)