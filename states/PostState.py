from aiogram.dispatcher.filters.state import State, StatesGroup


class PostState(StatesGroup):
    Content = State()
    Photo = State()