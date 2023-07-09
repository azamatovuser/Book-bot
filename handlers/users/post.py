from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.PostState import PostState
from data.config import ADMINS, BASE_URL
import requests


@dp.message_handler(commands=['send_post'])
async def send_post(message: types.Message):
    if message.from_user.id == int(ADMINS[0]):
        await bot.send_message(chat_id=message.chat.id, text="Reklama bo'ladigan xabarni jo'nating 👇🏻")
        await PostState.Content.set()
    else:
        await bot.send_message(chat_id=message.chat.id, text="Afsuski sizga mumkin emas ⛔️")


@dp.message_handler(state=PostState.Content)
async def handle_post_content(message: types.Message, state: FSMContext):
    rs = requests.get(url=f"{BASE_URL}user/list_create/")
    data = rs.json()
    post_content = message.text
    for user in data:
        await bot.send_message(chat_id=user['telegram_id'], text=post_content)
    await state.finish()
    await bot.send_message(chat_id=message.chat.id, text="Tabriklaymiz, post yuborildi! 🥳")