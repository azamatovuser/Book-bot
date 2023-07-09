from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.main_button import main_button
import requests
from loader import dp, bot
from data.config import BASE_URL, CHANNELS
from utils.misc import subscription
from keyboards.inline.subscription import check_button


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    data = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
    }
    requests.post(url=f"{BASE_URL}user/list_create/", data=data)
    is_subscribed = await subscription.check(user_id=telegram_id, channel=CHANNELS[0])
    if is_subscribed:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}! 🚀", reply_markup=main_button)
    else:
        channels_format = str()
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"

        await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n"
                             f"{channels_format}",
                             reply_markup=check_button,
                             disable_web_page_preview=True)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            await call.message.delete()
            await call.message.answer(f"Assalomu alaykum {call.from_user.full_name}! 🚀", reply_markup=main_button)
        else:
            invite_link = await channel.export_invite_link()
            result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    await call.message.answer(result, disable_web_page_preview=True)
