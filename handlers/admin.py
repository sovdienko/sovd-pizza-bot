from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
import logging
from create_bot import bot, dp
from database import db
from keyboard import kb_admin
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


#define a admin for making future aploading
#@dp.message_handler(commands='admin', is_chat_admin=True)
async def define_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(ID, 'Що повелитель побажає?', reply_markup=kb_admin.kb_admin)
    await message.delete()


#Початок потока завантаження даних про піцу
#@dp.message_handler(commands='Завантаження', state=None)
async def start_pizza_upload_flow(message: types.Message):
    if ID == message.from_user.id:
        await FSMAdmin.photo.set()
        await message.reply('Кидай сюди фото піци')


#Відміняємо поток завантаження даних
#@dp.message_handler(commands='Відміна', state="*")
#@dp.message_handler(Text(equals='відміна', ignore_case=True), state="*")
async def cancel_pizza_upload_flow(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('СТОП!')


#Отримуєм першу відповіть (фото) і кладемо її у словник
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    logging.info('start load_photo')
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Пиши назву піци")


#Отримуєм назву
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    logging.info('start load_name')
    if ID == message.from_user.id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Опиши піцу")


#Отримуєм опис
#@dp.message_handler(state=FSMAdmin.description)
async def load_desc(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Яка ціна піци?")


#Отримуєм ціну та завершуємо поток
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await db.add_menu(state)
        await state.finish()

#@dp.message_handler(commands='Видалити')
async def del_menu(message: types.Message):
    if ID == message.from_user.id:
        menu_list = await db.show_menu_del()
        for menu in menu_list:
            await bot.send_photo(message.from_user.id, menu[0], f'{menu[1]}\nОпис: {menu[2]}\nЦіна {menu[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(text=f'Видалити {menu[1]}', callback_data=f'del {menu[1]}')))


#@dp.callback_query_handler(Text(startswith='del '))
async def delete_menu_item(callback_query: types.CallbackQuery):
    menu_name = callback_query.data.replace('del ', '')
    await db.del_menu_item(menu_name)
    await callback_query.answer(text=f'{menu_name} видалена', show_alert=True)



def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start_pizza_upload_flow, commands='Завантаження', state=None)
    dp.register_message_handler(cancel_pizza_upload_flow, commands='Відміна', state="*")
    dp.register_message_handler(cancel_pizza_upload_flow, Text(equals='відміна', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_desc, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(define_admin, commands='admin', is_chat_admin=True)
    dp.register_message_handler(del_menu, commands='Видалити')
    dp.register_callback_query_handler(delete_menu_item, Text(startswith='del '))

