import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

from transliterate.discover import autodiscover
from transliterate.base import TranslitLanguagePack, registry
from transliterate import translit, detect_language

#Создание словаря и класса для перевода
ru = 'А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ы Ъ Э Ю Я'
en = 'A B V G D E E ZH Z I I K L M N O P R S T U F KH TS CH SH SHCH Y IE E IU IA'
full_list = list(zip(ru.split() + ru.lower().split(),en.split() + en.lower().split()))
dict_one_to_sev = dict(filter(lambda x: len(x[1]) == 2, full_list))
dict_one_to_sev.update({'Ь':'','ь':''})
dict_one_to_one = dict(filter(lambda x: len(x[1]) == 1, full_list))
tuple_one_to_one = (''.join(dict_one_to_one.keys()),''.join(dict_one_to_one.values()))

autodiscover()
class MID_RU(TranslitLanguagePack):
    language_code = "MID_RU"
    language_name = "MID RU"
    #Модуль translate позволяет создать собственный класс языка для перевода,
    #только немного странно - нужно отдельно указывать буквы транслитерующие 1 к 1 (кортеж строк) и 1 к нескольким (словарь)
    mapping = tuple_one_to_one
    pre_processor_mapping = dict_one_to_sev

registry.register(MID_RU)

TOKEN = os.getenv('TOKEN')
#TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO,filename='botlog.log')

@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'{user_name}, привет! Введите любое ФИО (текст) для перевода в латиницу по правилам МИД!'
    logging.info(f'{user_name} {user_id} start the bot!')
    await bot.send_message(chat_id = user_id, text = text)

@dp.message()
async def send_echo(message: Message):
    warning_fl = False
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    tr_text = translit(message.text.title(), language_code='MID_RU')
    if not message.text.replace(" ", "").isalpha() or detect_language(message.text) != 'ru':
        warning_fl = True
        await message.answer('ПРЕДУПРЕЖДЕНИЕ: В запросе присутствуют символы отличные от русских букв, результат может быть некорректен')
    logging.info(f'{user_name} {user_id}: {message.text} --> {tr_text}, Warning: {warning_fl}')
    await message.reply(text = f'{tr_text}')

if __name__ == '__main__':
    dp.run_polling(bot)