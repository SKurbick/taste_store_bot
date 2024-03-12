from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_reg1 = InlineKeyboardButton(text="Зарегистрироваться", callback_data="registration")
button_cancel1 = InlineKeyboardButton(text="Отменить", callback_data="cancel")
keyboard_registration = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_reg1, button_cancel1],
    ])

button_reg_user = InlineKeyboardButton(text="Зарегистрировать пользователя", callback_data="registration_user")
button_refuse_user = InlineKeyboardButton(text="Отказать в регистрации", callback_data="refuse_user")
keyboard_registration_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_reg_user],
        [button_refuse_user],
    ])

button_confirm = InlineKeyboardButton(text="Подтвердить", callback_data="confirm_data")
button_reset = InlineKeyboardButton(text="Сбросить регистрацию", callback_data="reset_data")

keyboard_confirm_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_confirm, button_reset],
    ]
)

button_buyer_role = InlineKeyboardButton(text="Закупщик", callback_data="buyers")
button_manager_role = InlineKeyboardButton(text="Менеджер(клиент)", callback_data="managers")

keyboard_role_give = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_buyer_role, button_manager_role],
    ]
)
