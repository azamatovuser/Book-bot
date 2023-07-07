from aiogram import types
from loader import dp, bot
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
from data.config import BASE_URL
from keyboards.default.main_button import main_button
from requests.exceptions import RequestException


@dp.message_handler(text='Kitoblar')
async def list(message: types.Message):
    books = ReplyKeyboardMarkup(resize_keyboard=True)
    rs = requests.get(url=f"{BASE_URL}book/list/")
    data = rs.json()
    for book in data:
        books.add(book['title'])
    books.add('Menu')
    await message.answer(f"Qaysi kitobni tanlaysiz?", reply_markup=books)


@dp.message_handler(text='Menu')
async def back(message: types.Message):
    await message.answer(f"Orqaga qaytdingiz", reply_markup=main_button)


@dp.message_handler()
async def handle_book_request(message: types.Message):
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
        elif response.status_code == 404:
            await message.reply("Book not found.")
        else:
            await message.reply("Error occurred while retrieving the book.")
    except RequestException:
        await message.reply("Error occurred while making the API request.")