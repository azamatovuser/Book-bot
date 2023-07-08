from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )