from aiogram import types
from loader import dp, bot
from data.config import BASE_URL, ADMINS
from keyboards.default.statistic_button import statistic_button
from aiogram.types import ReplyKeyboardRemove
import requests


@dp.message_handler(commands='statistic')
async def get(message: types.Message):
    if message.from_user.id != int(ADMINS[0]):
        await message.answer('Sizga mumkin emas ⛔️')
    else:
        await message.answer('Qaysi biri?', reply_markup=statistic_button)


@dp.message_handler(text='Haftalik statistika 📊')
async def week(message: types.Message):
    if message.from_user.id != int(ADMINS[0]):
        await message.answer('Sizga mumkin emas ⛔️')
    else:
        rs = requests.get(url=f"{BASE_URL}user/statistic/week/")
        data = rs.json()
        count = 0
        for i in data:
            count += 1
        await message.answer(f"Oxirgi bir haftada - {count} userlar qo'shilgan 🧑🏻‍💻")


@dp.message_handler(text='Oylik statistika 🗓')
async def month(message: types.Message):
    if message.from_user.id != int(ADMINS[0]):
        await message.answer('Sizga mumkin emas ⛔️')
    else:
        rs = requests.get(url=f"{BASE_URL}user/statistic/month/")
        data = rs.json()
        count = 0
        for i in data:
            count += 1
        await message.answer(f"Oxirgi bir oyda - {count} userlar qo'shilgan 🧑🏻‍💻")


@dp.message_handler(text='Umumiy 📤')
async def month(message: types.Message):
    if message.from_user.id != int(ADMINS[0]):
        await message.answer('Sizga mumkin emas ⛔️')
    else:
        rs = requests.get(url=f"{BASE_URL}user/list_create/")
        data = rs.json()
        count = 0
        for i in data:
            count += 1
        await message.answer(f"Umumiy - {count} userlar bor 🧑🏻‍💻")


@dp.message_handler(text='Yopish ⬅️')
async def close(message: types.Message):
    await message.answer("Yopildi ✅", reply_markup=ReplyKeyboardRemove())