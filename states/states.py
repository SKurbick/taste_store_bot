from aiogram.fsm.state import StatesGroup, State


class FSMCommOffer(StatesGroup):
    product_name = State()
    unit = State()
    upload_photo = State()
    country = State()
    comments = State()
    price = State()
    yes_no = State()


class FSMRegistration(StatesGroup):
    user_name = State()
    phone_number = State()
    telegram_username = State()
    yes_no = State()


class FSMWaitingForRegUser(StatesGroup):
    user_role = State()


class FSMDeleteUser(StatesGroup):
    user_id = State()
    yes_or_no = State()
    finish = State()