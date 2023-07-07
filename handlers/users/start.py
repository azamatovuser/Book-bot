from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.main_button import main_button
import requests
from loader import dp, bot
from data.config import BASE_URL, CHANNELS
from utils.misc import checking_system
from keyboards.inline.subscription import check_button


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # channels_format = str()
    # for channel in CHANNELS:
    #     chat = await bot.get_chat(channel)
    #     invite_link = await chat.export_invite_link()
    #     channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
    #
    # await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n"
    #                      f"{channels_format}",
    #                      reply_markup=check_button,
    #                      disable_web_page_preview=True)
    telegram_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    data = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
    }
    rs = requests.post(url=f"{BASE_URL}user/list_create/", data=data)
    print(rs)
    await message.answer(f"Assalamu alaykum {message.from_user.full_name}!", reply_markup=main_button)
