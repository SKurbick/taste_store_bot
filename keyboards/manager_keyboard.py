from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_order = InlineKeyboardButton(text="Заказать", callback_data="order")
button_skip = InlineKeyboardButton(text="Пропустить(скрыть)", callback_data="skip")
keyboard_order_or_skip = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_order, button_skip],
    ]
)
button_show_offers = InlineKeyboardButton(text="Показать!", callback_data="show_all_offers")
button_cancel = InlineKeyboardButton(text="Не сейчас", callback_data="cancel_show_offers")

keyboard_show_all_offers = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_show_offers, button_cancel],
    ]
)