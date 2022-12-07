from aiogram import Dispatcher, types
import json
import string


'''перевірка чи є слово матюком'''
def is_bad_word(message: types.Message):
    if {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in message.text.split(' ')} \
            .intersection(set(json.load(open("cenz.json")))) != set():
        return True
    return False


#@dp.message_handler(lambda message: 'ку' in message.text)
async def secret_command(message: types.Message):
    await message.answer('Бінго!!!')


#@dp.message_handler(is_bad_word(message))
async def echo_send(message: types.Message):
    if {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in message.text.split(' ')} \
            .intersection(set(json.load(open("cenz.json")))) != set():
        await message.reply("Матюки тут заборонені")
        await message.delete()


#@dp.message_handler()
async def no_command(message: types.Message):
    await message.reply("Такої команди не існує!")



def register_others_handlers(dp: Dispatcher):
    dp.register_message_handler(secret_command, lambda message: 'ку' in message.text)
    dp.register_message_handler(echo_send, lambda message: is_bad_word(message))
    dp.register_message_handler(no_command)