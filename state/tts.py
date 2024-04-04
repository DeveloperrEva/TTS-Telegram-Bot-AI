from aiogram.dispatcher.filters.state import State, StatesGroup

class male(StatesGroup):
    text = State()
    
class female(StatesGroup):
    text = State()