import asyncio
import executor
from tok import key, apiKey
import aiogram
from aiogram import Bot, Dispatcher, types
import requests
import json

bot = Bot(key)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def info(message:types.Message):
    markup = type.InlineKeyboardMarkup()
    markup.add(type.InlineKeyboardButton('Получить прогноз погоды', callback_data='city'))
    markup.add(type.InlineKeyboardButton('Получить прогноз погоды', callback_data='list'))
    await message.reply('Привет, здесь ты можешь узнать прогноз погоды!', reply_markup=markup)

@dp.message_handler(commands=['listCity'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(type.InlineKeyboardButton('Москва'))
    markup.add(type.InlineKeyboardButton('Санкт-Петербург'))
    await message.reply('Привет!', reply_markup=markup)

@dp.callback_query_handler()
async def callback(call):
    if call.data == 'list':
        await call.message.answer('/listCity\n/start')
    elif call.data == 'city':
        await call.message.answer('Введите город')

@dp.message_handler(commands=['text'])
async def reply(message:types.Message):
    city = message.text.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={apiKey}'
    res = requests.get(url)
    data = json.loads(res.text)
    if res.status_code == 200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        desc = data['weather'][0]['description']
        await message.reply(f'Погода в городе {message.text}\n'
                            f'Температура {temp}\n'
                            f'Влажность {humidity}%\n'
                            f'Давление {pressure}PA\n'
                            f'Ветер {wind_speed} м/с\n'
                            f'Описание {desc}')
    elif res.status_code == 404:
        await message.reply('Город не найден.')

executor.start_polling(dp)