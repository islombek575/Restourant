from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, KeyboardButton

from bot.buttuns.buttuns import make_inline_btn, make_reply_btn
from bot.database.models import Category
from bot.states import RestourantState

back_router = Router()

@back_router.callback_query(RestourantState.res_menu, F.data == "back_to_main")
async def back_handler(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    btns = [
        KeyboardButton(text="🍽 Restoran Menyusi"),
        KeyboardButton(text="📞 Biz Bilan Bog'lanish")
    ]
    markup = make_reply_btn(btns, [2])
    await state.set_state(RestourantState.main)
    await state.clear()
    await call.message.answer(text="🏠 Asosiy Menyu", reply_markup=markup)

@back_router.callback_query(RestourantState.subcategories, F.data == "back_to_res_main")
async def back_handler(call:CallbackQuery, state:FSMContext):
    categories: list[Category] = await Category().get_all()
    btns = [InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}") for category in categories]
    btns.append(InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_main"))
    markup = make_inline_btn(btns, [2])
    await state.set_state(RestourantState.res_menu)
    await call.message.edit_text("🍽 Restoran Menyusi", reply_markup=markup)
