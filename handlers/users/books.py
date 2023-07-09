from aiogram import types
from loader import dp, bot
from aiogram.types import ReplyKeyboardMarkup
import requests
from data.config import BASE_URL
from keyboards.default.main_button import main_button
from requests.exceptions import RequestException
import asyncio


@dp.message_handler(text='Kitoblar 📚')
async def list(message: types.Message):
    books = ReplyKeyboardMarkup(resize_keyboard=True)
    rs = requests.get(url=f"{BASE_URL}book/list/")
    data = rs.json()
    for book in data:
        books.add(book['title'])
    books.add('Menu ⬅️')
    await message.answer(f"Qaysi kitobni tanlaysiz? 🤔", reply_markup=books)


@dp.message_handler(text='Menu ⬅️')
async def back(message: types.Message):
    await message.answer(f"Orqaga qaytdingiz ✅", reply_markup=main_button)


@dp.message_handler()
async def handle_book_request(message: types.Message):
    temporary_response = await message.answer("Kitob qidirilmoqda 🔎")
    book_title = message.text
    url = f"{BASE_URL}book/detail/"
    params = {'title': book_title}
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            file_path = data.get('file')
            with open(file_path, 'rb') as file:
                await bot.send_document(message.chat.id, file, caption=book_title)
            await temporary_response.delete()
        elif response.status_code == 404:
            await asyncio.sleep(2)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=temporary_response.message_id, text="Bizning ma'lumot omborimizda bunday kitob mavjud emas")
        else:
            await temporary_response.delete()
            await bot.edit_message_text(chat_id=message.chat.id, message_id=temporary_response.message_id, text='Tizimda xatolik, iltimos oz vaqt kuting')
    except RequestException:
        await temporary_response.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=temporary_response.message_id, text='Tizimda xatolik, iltimos oz vaqt kuting')