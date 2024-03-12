from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import LEXICON_RU

button_0 = KeyboardButton(text=LEXICON_RU['comm_offer_button'])
comm_offer_kb = ReplyKeyboardMarkup(
    keyboard=[
        [button_0]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,

)

button_thing = InlineKeyboardButton(text="за штуку", callback_data="thing")
button_kg = InlineKeyboardButton(text="за килограмм", callback_data="kg")

keyboard_unit = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_kg, button_thing],
    ])

button_yes = InlineKeyboardButton(text="Подтвердить", callback_data="yes")
button_no = InlineKeyboardButton(text="Отменить", callback_data="no")
keyboard_yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_yes, button_no],
    ],
)

button_show_offers = InlineKeyboardButton(text="Показать!", callback_data="show_my_offers")
button_cancel = InlineKeyboardButton(text="Не сейчас", callback_data="cancel_show_offers")

keyboard_show_my_offers = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_show_offers, button_cancel],
    ]
)
