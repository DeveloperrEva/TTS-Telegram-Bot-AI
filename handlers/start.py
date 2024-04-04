from main import *
import aiohttp
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from data import db
from state import male, female

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state="*"):
    db.join(chat_id=message.from_user.id, username=message.from_user.username, firstname=message.from_user.first_name, date=today)
    await state.finish()
    gender = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Мужской", callback_data="male")
    item2 = InlineKeyboardButton("Женский", callback_data="female")
    gender.add(item1, item2)
    await message.answer("Выберите пол", reply_markup=gender)
    
@dp.callback_query_handler(lambda c: c.data == "male")
async def male_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Отправьте текст")
    await male.text.set()

@dp.message_handler(state=male.text, content_types=['text'])
async def process_messages(message: types.Message, state: FSMContext):
    text = message.text
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.RECORD_AUDIO)
    url = "https://api.elevenlabs.io/v1/text-to-speech/29vD33N1CtxCmqQRPOHJ"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": config.XI_API_KEY
    }

    data = {
        "text": f"{text}",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            filename = f'./voices/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp3'
            with open(filename, 'wb') as f:
                async for chunk in response.content.iter_any():
                    f.write(chunk)

    voice_message = types.InputFile(filename)
    await bot.send_voice(chat_id=message.chat.id, voice=voice_message)
    await state.finish()
    
@dp.callback_query_handler(lambda c: c.data == "female")
async def female_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Отправьте текст")
    await female.text.set()

@dp.message_handler(state=female.text, content_types=['text'])
async def process_messages(message: types.Message, state: FSMContext):
    text = message.text
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.RECORD_AUDIO)
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": config.XI_API_KEY
    }

    data = {
        "text": f"{text}",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            filename = f'./voices/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp3'
            with open(filename, 'wb') as f:
                async for chunk in response.content.iter_any():
                    f.write(chunk)

    voice_message = types.InputFile(filename)
    await bot.send_voice(chat_id=message.chat.id, voice=voice_message)
    await state.finish()