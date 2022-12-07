from aiogram import executor
from create_bot import dp
from handlers import client, admin, others
from database import db

import logging


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    logging.info("Бот вийшов в онлайн")
    db.db_start()


client.register_client_handlers(dp)
admin.register_admin_handlers(dp)
others.register_others_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
