from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_show_buyer = InlineKeyboardButton(text="Закупщики", callback_data="show_buyers")
button_show_manager = InlineKeyboardButton(text="Менеджеры", callback_data="show_managers")
keyboard_show_users = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_show_buyer, button_show_manager],
    ],
)

button_know_user_id = InlineKeyboardButton(text="Знаю id пользователя", callback_data="know_user_id")
keyboard_know_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_know_user_id],
    ],
)

button_delete_buyer = InlineKeyboardButton(text="Удалить", callback_data="delete_user")
button_cancel_delete = InlineKeyboardButton(text="Отмена", callback_data="cancel_delete")
keyboard_delete_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_delete_buyer, button_cancel_delete],
    ],
)
