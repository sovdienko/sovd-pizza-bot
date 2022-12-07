from aiogram import Bot, Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)
