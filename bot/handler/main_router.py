from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, CallbackQuery, InlineKeyboardButton

from bot.buttuns.buttuns import make_reply_btn, make_inline_btn
from bot.database.models import Category, Product
from bot.states import RestourantState

main_router = Router()

@main_router.message(CommandStart())
async def start_handler(message:Message, state:FSMContext):
    btns = [
        KeyboardButton(text="🍽 Restoran Menyusi"),
        KeyboardButton(text="📞 Biz Bilan Bog'lanish"),
    ]
    markup = make_reply_btn(btns,[2])
    await state.set_state(RestourantState.main)
    await message.answer(text="🏠 Asosiy Menyu",reply_markup=markup)

@main_router.message(F.text=="🍽 Restoran Menyusi")
async def res_manu_handler(message:Message, state:FSMContext):
    categories: list[Category] = await Category().get_all()
    btns = [InlineKeyboardButton(text=category.name,callback_data=f"category_{category.id}") for category in categories]
    btns.append(InlineKeyboardButton(text="⬅️ Back",callback_data="back_to_main"))
    markup = make_inline_btn(btns,[2])
    await state.set_state(RestourantState.res_menu)
    await message.answer("🍽 Restoran Menyusi",reply_markup=markup)

@main_router.callback_query(F.data.startswith("category_"), RestourantState.res_menu)
async def res_manu_handler(call:CallbackQuery, state:FSMContext):
    category_id = int(call.data.split("_")[-1])
    products: list[Product] = await Product().get_with_id("category_id",category_id)
    btns = [InlineKeyboardButton(text=product.name,callback_data=f"product_{product.id}")for product in products]
    btns.append(InlineKeyboardButton(text="⬅️ Back",callback_data="back_to_res_main"))
    markup = make_inline_btn(btns,[2])
    await state.set_state(RestourantState.subcategories)
    await call.message.edit_text("🥗 Salatlar (Taom Tanlash)",reply_markup=markup)


@main_router.callback_query(F.data.startswith("product_"), RestourantState.subcategories)
async def product_handler(call:CallbackQuery , state:FSMContext):
    product_id = int(call.data.split("_")[-1])
    product: Product = await Product().get(product_id)
    await state.set_state(RestourantState.main)
    res = ""
    description = product.description.split(",")
    for desc in description:
        res+=desc+"\n"
    if not product.photo:
        await call.message.edit_text(text=f"{description}")
    else:
        await call.message.delete()
        await call.message.answer_photo(photo=product.photo,caption=res)


