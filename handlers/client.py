from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from keyboard.kb_client import kb_client
from database import db


# @dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Смачного", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Спілкування з ботом тільки через Direct, пишіть йому "
                            "\nhttps://t.me/SovdPizzaBot")


# @dp.message_handler(commands=['Режим_роботи'])
async def schedule_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Цілодобово")


# @dp.message_handler(commands=['Наша_адреса'])
async def location_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Київ, вул. Метрологічна, 20ї")


# @dp.message_handler(commands=['Меню'])
async def menu_command(message: types.Message):
    await db.show_menu(message)


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(menu_command, commands=['Меню'])
    dp.register_message_handler(schedule_command, commands=['Режим_роботи'])
    dp.register_message_handler(location_command, commands=['Наша_адреса'])

