from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btUpload = KeyboardButton('/Завантаження')
btDelete = KeyboardButton('/Видалити')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin.add(btUpload).add(btDelete)
