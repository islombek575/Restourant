from aiogram.fsm.state import StatesGroup, State


class RestourantState(StatesGroup):
    main = State()
    res_menu = State()
    subcategories = State()

