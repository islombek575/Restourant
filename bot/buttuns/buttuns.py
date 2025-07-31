from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def make_reply_btn(btns,sizes):
    builder = ReplyKeyboardBuilder()
    builder.add(*btns)
    if sizes:
        builder.adjust(*sizes)
    else:
        builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def make_inline_btn(btns,sizes):
    builder = InlineKeyboardBuilder()
    builder.add(*btns)
    if sizes:
        builder.adjust(*sizes)
    else:
        builder.adjust(1)
    return builder.as_markup()