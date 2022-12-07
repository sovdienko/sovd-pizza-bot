import sqlite3
import logging
from aiogram import types
from create_bot import bot


def db_start():
    global conn, cursor
    conn = sqlite3.connect("sovd_pizza.db")
    cursor = conn.cursor()
    if conn:
        logging.info("Database connected!")
    cursor.execute("create table if not exists menu(img text, name text primary key, description text, price text)")


async def add_menu(state):
    async with state.proxy() as data:
        cursor.execute("insert into menu (img, name, description, price) values(?, ?, ?, ?)", tuple(data.values()))
        conn.commit()


async def show_menu(message: types.Message):
    for ret in cursor.execute("select img, name, description, price from menu").fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nДеталі: {ret[2]}\nЦіна: {ret[-1]}')


async def show_menu_del():
    return cursor.execute("select img, name, description, price from menu").fetchall()


async def del_menu_item(name):
    cursor.execute("delete from menu where name = ?", (name,))
    conn.commit()
