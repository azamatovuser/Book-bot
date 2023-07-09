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
    await state.update_data(message_text=message.text)
    if message.entities:
        await state.update_data(entities=message.entities[0].url)
    await PostState.Photo.set()
    await message.answer("Endi rasmni jo'nating agar bo'lmasa 'yo'q' degan so'zni yozing")


@dp.message_handler(content_types=types.ContentType.PHOTO, state=PostState.Photo)
async def handle_post_photo(photo: types.File, state: FSMContext):
    rs = requests.get(url=f"{BASE_URL}user/list_create/")
    data = rs.json()
    message_data = await state.get_data()
    post_content = message_data.get('message_text')
    entities = message_data.get('entities')

    if entities:
        button = types.InlineKeyboardMarkup(row_width=True)
        link = types.InlineKeyboardButton("Ochib ko'rish", url=entities)
        button.add(link)
        for user in data:
            await bot.send_photo(chat_id=user['telegram_id'], photo=photo.photo[0].file_id, caption=post_content, reply_markup=button)
    else:
        for user in data:
            await bot.send_photo(chat_id=user['telegram_id'], photo=photo.photo[0].file_id, caption=post_content)

    await state.finish()
    await bot.send_message(chat_id=int(ADMINS[0]), text="Tabriklaymiz, post yuborildi! 🥳")


@dp.message_handler(state=PostState.Photo)
async def handle_no_photo(message: types.Message, state: FSMContext):
    if message.text.lower() == "yo'q":
        rs = requests.get(url=f"{BASE_URL}user/list_create/")
        data = rs.json()
        message_data = await state.get_data()
        post_content = message_data.get('message_text')
        entities = message_data.get('entities')

        if entities:
            button = types.InlineKeyboardMarkup(row_width=True)
            link = types.InlineKeyboardButton("Ochib ko'rish", url=entities)
            button.add(link)
            for user in data:
                await bot.send_message(chat_id=user['telegram_id'], text=post_content, reply_markup=button)
        else:
            for user in data:
                await bot.send_message(chat_id=user['telegram_id'], text=post_content)

        await state.finish()
        await bot.send_message(chat_id=int(ADMINS[0]), text="Tabriklaymiz, post yuborildi! 🥳")
    else:
        await message.reply("Tizimda xatolik, iltimos oz vaqt kuting")