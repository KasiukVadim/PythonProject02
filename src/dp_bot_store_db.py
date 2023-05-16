import db
from keyboard import *
from config import TOKEN_API
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

data_base = db.DB()

storage = MemoryStorage()
bot = Bot(TOKEN_API)
#dp = Dispatcher(bot, storage=storage)
