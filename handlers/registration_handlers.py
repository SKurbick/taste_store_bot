
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery,  InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.filters import Command

from filters.data_validate import IsPhoneNumber, IsUserName
from keyboards.registration_keyboard import keyboard_registration, keyboard_confirm_data
from lexicon.lexicon import LEXICON_RU


from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.states import FSMRegistration
from filters.all_users import IsRegUsersMessage
from utils import  users_list, add_in_waiting_for_reg

# todo хендлер реагирует на сообщение ответным сообщением о том что пользвоателю необходимо зарегистрироваться, если его в ролевых списках
admin = users_list("admins")[0]
router = Router()
router.message.filter(~IsRegUsersMessage())


@router.message(Command(commands="registration"), StateFilter(default_state))
async def registration(message: Message):
    await message.answer(text="Подтвердите запрос на регистрацию:",
                         reply_markup=keyboard_registration)


@router.callback_query(F.data.in_(["registration", "cancel"]), StateFilter(default_state))
async def registration_status(callback: CallbackQuery, state: FSMContext):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    if callback.data == "registration":
        await callback.message.answer(text="Давайте зарегистрируемся!\nПредставьтесь, пожалуйста: формат - Иван Иванов")
        await state.set_state(FSMRegistration.user_name)

    if callback.data == "cancel":
        await callback.message.answer(text="Вы отменили регистрацию.")


@router.message(StateFilter(FSMRegistration.user_name), IsUserName())
async def reg_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(text=LEXICON_RU["reg_username"].format(message.text))
    await state.set_state(FSMRegistration.phone_number)


@router.message(StateFilter(FSMRegistration.user_name))
async def wrong_reg_username(message: Message):
    await message.answer(text="То что вы отправили не похоже на имя и фамилию")


@router.message(StateFilter(FSMRegistration.phone_number), IsPhoneNumber())
async def reg_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer(text=LEXICON_RU['reg_phone_number'], reply_markup=keyboard_confirm_data)
    await state.set_state(FSMRegistration.yes_no)


@router.message(StateFilter(FSMRegistration.phone_number))
async def wrong_reg_phone_number(message: Message):
    await message.answer(text="То что вы отправили не похоже на номер мобильного телефона")


@router.callback_query(StateFilter(FSMRegistration.yes_no), F.data.in_(["confirm_data", "reset_data"]))
async def phone_number(callback: CallbackQuery, state: FSMContext):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    button_reg_user = InlineKeyboardButton(text="Зарегистрировать",
                                           callback_data=f"registration_{callback.from_user.id}")
    button_refuse_user = InlineKeyboardButton(text="Отказать",
                                              callback_data=f"refuse_{callback.from_user.id}")
    keyboard_registration_user_test = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_reg_user, button_refuse_user],
        ])

    if callback.data == "confirm_data":
        state_data = await state.get_data()
        reg_user_data = {
            "reg_user_name": state_data["username"],
            "link_username": callback.from_user.username,
            "phone_number": state_data["phone_number"]
        }
        await callback.bot.send_message(chat_id=admin,
                                        text=LEXICON_RU["/registration_action"].format(reg_user_data["reg_user_name"],
                                                                                       reg_user_data["phone_number"]),
                                        reply_markup=keyboard_registration_user_test)
        await callback.message.answer(text=LEXICON_RU["/registration_status"])

        # добавляем в БД в список ожидания (waiting_for_reg.json)
        add_in_waiting_for_reg(callback.from_user.id, reg_user_data)
        await state.clear()
    if callback.data == "reset_data":
        await callback.message.answer(text="Вы отменили регистрацию.")
        await state.clear()


@router.message()
async def pre_registration_message(message: Message):
    await message.answer(
        text="Вам необходимо зарегистрироваться. Отправьте команду /registration и с вами свяжется администратор "
             "компании 'ОФК'")
