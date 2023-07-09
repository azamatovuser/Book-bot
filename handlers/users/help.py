from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Yordam beruvchi komandalar: ",
            "/start - Ishga tushurish",
            "/help - Yordam",
            "/send_post - Reklama berish",
            "/statistic - Kanalni statistikasi",
            )
    
    await message.answer("\n".join(text))
