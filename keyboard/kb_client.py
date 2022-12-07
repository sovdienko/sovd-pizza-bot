from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btSchedule = KeyboardButton('/Режим_роботи')
btLocation = KeyboardButton('/Наша_адреса')
btMenu = KeyboardButton('/Меню')
btSharePhone = KeyboardButton('Поділитися контактом', request_contact=True)
btShareLocation = KeyboardButton('Поділітися місцеположенням', request_location=True)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(btMenu).row(btLocation, btSchedule).row(btSharePhone, btShareLocation)
