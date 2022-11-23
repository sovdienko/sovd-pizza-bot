from aiogram import Bot, Dispatcher, executor, types

import os
import logging
import string
import json

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    logging.info("Бот вийшов в онлайн")


"""================================= CLIENT =========================================="""


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Смачного")
        await message.delete()
    except:
        await message.reply("Спілкування з ботом тільки через Direct, пишіть йому \nhttps://t.me/SovdPizzaBot")


@dp.message_handler(commands=['Режим_роботи'])
async def schedule_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Цілодобово")


@dp.message_handler(commands=['Наша_адреса'])
async def schedule_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Київ, вул. Метрологічна, 20ї")


"""================================= ADMIN ==========================================="""

"""================================= COMMON =========================================="""


@dp.message_handler()
async def echo_send(message: types.Message):
    if {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in message.text.split(' ')} \
            .intersection(set(json.load(open("cenz.json")))) != set():
        await message.reply("Матюки тут заборонені")
        await message.delete()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
