from aiogram.types import ReplyKeyboardMarkup

statistic_button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
statistic_button.add('Haftalik statistika 📊', 'Oylik statistika 🗓', 'Umumiy 📤', 'Yopish ⬅️')