import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from models import Weather, Exchange

import api
from api import get_weather, get_exchange_rate
from config import API_TOKEN, EXCHANGERATE_API_KEY
from keyboard import kb, kb2, ikb
import os
import random
from random import randrange

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
HELP_COMMAND = """
<b>/start</b> - запустить бота
<b>/help</b> - список команд
<b>/description</b> - описание бота
<b>/sticker</b> - отправка стикера
<b>/photo</b> - отправка фотографии
<b>/exchange</b> - конвертация валют
<b>/weather</b> - погода
<b>/poll</b> - опрос
<b>/location</b> - отправка геолокации"""

photo_urls = [
    'https://sport-dog.ru/wp-content/uploads/a/9/c/a9cd06f48ea5f6a612ce83eed1178111.jpeg',
    'https://i.pinimg.com/originals/ba/70/a3/ba70a3e6894d90df6b3e7286979a6d02.jpg',
    'https://oir.mobi/uploads/posts/2020-04/1586438141_23-p-malenkie-lvyata-51.jpg',
    'https://ieducations.ru/wp-content/uploads/7/3/6/73654d69e0150a7fedfe7981cc712373.jpeg',
    'https://images.ua.prom.st/746701748_w640_h640_zameniteli-moloka-dlya.jpg',
    'https://klike.net/uploads/posts/2023-01/1674294415_3-53.jpg',
]

answers = ["Red", "Blue", "Green", "Yellow", "Purple"]

async def on_startup(_):
    print("I have been started")

@dp.message_handler(commands=['start'])
async def get_start(message: types.Message):
    await message.answer(text="Добро пожаловать в наш чат-бот",
                                        reply_markup=kb)
    await message.delete()

@dp.message_handler(commands=['help'])
async def get_help(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                                        parse_mode='HTML',
                                        reply_markup=kb2)
    await message.delete()


@dp.message_handler(commands=['description'])
async def get_descr(message: types.Message):
    await message.answer(text="<em>Это тестовый вариант бота. Сейчас он находится на стадии разработки.</em>",
                                        parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    await message.answer(text="<em>Enter a city name:</em>", parse_mode='HTML')

    @dp.message_handler()
    async def process_city(message: types.Message):
        city = message.text
        current_weather = await api.get_weather(city)

        if current_weather is not None:
            weather_text = f"Current weather in {current_weather.city}: {current_weather.description}. Temperature: {current_weather.temperature} K"
        else:
            weather_text = "Sorry, I couldn't find weather information for that city."

        await message.answer(text=weather_text)
        await message.delete()


    await dp.register_next_step_handler(message, process_city)


@dp.message_handler(commands=['exchange'])
async def get_exchange(message: types.Message):
    await message.answer(text="<em>Enter base currency and target currency (e.g. USD EUR):</em>", parse_mode='HTML')

    @dp.message_handler()
    async def process_currencies(message: types.Message):
        currencies = message.text.split()
        if len(currencies) != 2:
            await message.answer(text="<em>Please enter two currencies separated by a space.</em>", parse_mode='HTML')
            return

        base_currency, target_currency = currencies
        exchange_rate = await api.get_exchange_rate(base_currency, target_currency)

        if exchange_rate is not None:
            rate_text = f"1 {base_currency} = {exchange_rate} {target_currency}"
        else:
            rate_text = "Sorry, I couldn't get the exchange rate for those currencies."

        await message.answer(text=rate_text)
        # await message.delete()


    await dp.register_message_handler(process_currencies)# Use register_message_handler instead of register_next_step_handler



@dp.message_handler(commands=['sticker'])
async def get_sticker(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                                            text="Посмотри, какой он милый :3")
    await bot.send_sticker(chat_id=message.from_user.id,
                                        sticker="CAACAgIAAxkBAAEHf0Rj1i6MiddHiz2cz2Z_CdtvaojisQACOwADO2AkFFKC45_2IelfLQQ")
    await message.delete()

@dp.message_handler(commands=['photo'])
async def get_photo(message: types.Message):
    photo_url = random.choice(photo_urls)
    await bot.send_photo(message.from_user.id, photo_url, caption='Нравится эта фотография?', reply_markup=ikb)

@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer('Вам понравилась эта фотография!')
    elif  callback.data == 'dislike':
        await callback.answer('Вам не понравилась эта фотография.')
    elif callback.data == 'random':
        photo = random.choice(photo_urls)
        await callback.message.answer_photo(photo, caption='А как тебе эта?', reply_markup=ikb)
    elif callback.data == 'menu':
        await callback.message.answer(text=HELP_COMMAND,
                                        parse_mode='HTML',
                                        reply_markup=kb)

@dp.message_handler(commands=['location'])
async def get_loco(message: types.Message):
    await bot.send_location(message.from_user.id,
                                        longitude=randrange(1, 100),
                                        latitude=randrange(1, 100))
    await message.delete()

@dp.message_handler(commands=['poll'])
async def get_poll(update: types.Update):
    poll = await bot.send_poll(chat_id=428961894,
                               question="What's your favourite colour?",
                               is_anonymous=False,
                               options=answers)
    return poll


if __name__=="__main__":
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)