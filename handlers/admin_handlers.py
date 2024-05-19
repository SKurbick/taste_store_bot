from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from filters.data_validate import IsUserID
from keyboards.admin_keyboard import keyboard_show_users, keyboard_know_user, keyboard_delete_user
from keyboards.registration_keyboard import keyboard_role_give
from lexicon.lexicon import LEXICON_RU, help_message, command_role
from filters.is_admin import IsAdminMessage, IsAdminCallback
from utils import (users_list, give_role_and_save_in_db, get_data_in_waiting, add_user_in_role, del_waiting_data, \
                   show_all_users, search_user_role, delete_user_in_db, show_user_info, clear_offer_data)

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from states.states import FSMWaitingForRegUser, FSMDeleteUser

router = Router()
router.message.filter(IsAdminMessage())
router.callback_query.filter(IsAdminCallback())


# router.startup.register(admin_menu)


@router.message(Command(commands="what_status"))
async def what_status(message: Message):
    await message.answer(text="Вы Администратор")


@router.message(Command(commands="commands"))
async def help_bayer_message(message: Message):
    await message.answer(text=command_role["command_admin"])


@router.callback_query(F.data.startswith("registration_"), StateFilter(default_state))
async def registration_user(callback: CallbackQuery, state: FSMContext):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    reg_user_id = callback.data.split("_")[1]
    await state.update_data(user_id=reg_user_id)
    await callback.message.answer(text=LEXICON_RU["role_give"], reply_markup=keyboard_role_give)

    await state.set_state(FSMWaitingForRegUser.user_role)


@router.callback_query(StateFilter(FSMWaitingForRegUser), F.data.in_(["buyers", "managers"]))
async def role_give(callback: CallbackQuery, state: FSMContext):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    user_id_state_data = await state.get_data()
    user_id = user_id_state_data['user_id']

    user_role = callback.data
    "получаем данные по id из списка ожидания"
    user_data = get_data_in_waiting(user_id=user_id)
    "добавляем в инфо данные о пользователе"
    give_role_and_save_in_db(user_id=user_id, role=user_role, user_data=user_data)
    "добавляем в простой список id по фильтру роли"
    add_user_in_role(user_id=user_id, role=user_role)

    del_waiting_data(str(user_id))
    await callback.message.answer(text=f"Готово! Пользователь {user_data['reg_user_name']} успешно зарегистрирован!")
    await callback.bot.send_message(chat_id=user_id,
                                    text="Вы зарегистрированы! Отправьте команду /help для дальнейшего ознакомления.")
    await state.clear()


@router.callback_query(F.data.startswith("refuse_"), StateFilter(default_state))
async def refuse_user(callback: CallbackQuery):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    reg_user_id = callback.data.split("_")[1]
    del_waiting_data(str(reg_user_id))
    await callback.bot.send_message(chat_id=reg_user_id,
                                    text="Вам отказали в регистрации :(. Свяжитесь с менеджером компании для прояснения ситуации.")


@router.message(Command(commands="help"))
async def help_admin_message(message: Message):
    await message.answer(text=help_message["help_admin"])


@router.message(Command(commands="show_all_users"))
async def select_role_show(message: Message):
    await message.answer(text=LEXICON_RU['/show_all_users'], reply_markup=keyboard_show_users)


@router.callback_query(F.data.startswith("show_"))
async def show_users(callback: CallbackQuery):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    role = callback.data.split("_")[1]
    users_info = show_all_users(role)
    if users_info:
        # message_for_admin = str()
        # count = 0
        for user_info in users_info:
            # count += 1
            # message_for_admin += user_info
            # message_for_admin += '\n'
            # if count == 2:
            await callback.message.answer(text=user_info)
        # count = 0
        # message_for_admin = str()
    else:
        await callback.message.answer(
            text="Я не нашел выбранный список пользователей :(. Возможно никто еще с этой ролью не зарегистрирован")


@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def cancel_comm_offer(message: Message, state: FSMContext):
    await message.answer(text="Вы отменили действие")
    await state.clear()


@router.message(Command(commands="delete_user"), StateFilter(default_state))
async def delete_user(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/delete_user'], reply_markup=keyboard_know_user)
    await state.set_state(FSMDeleteUser.user_id)


@router.callback_query(F.data.in_(["know_user_id"]), StateFilter(FSMDeleteUser.user_id))
async def delete_user_know_id(callback: CallbackQuery, state: FSMContext):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    await callback.message.answer(text="Отлично. Отправьте user_id либо команду /cancel что бы отменить удаление")
    await state.set_state(FSMDeleteUser.yes_or_no)


@router.message(StateFilter(FSMDeleteUser.yes_or_no), IsUserID())
async def delete_user_yes_no(message: Message, state: FSMContext):
    user_id = message.text
    user_role = search_user_role(user_id)
    if user_role:
        user_data = show_user_info(user_role, user_id)
        await message.answer(text=LEXICON_RU['delete_user_finish'].format(user_data['reg_user_name']),
                             reply_markup=keyboard_delete_user)
        await state.update_data(user_id=user_id, user_role=user_role)
        await state.set_state(FSMDeleteUser.finish)
    else:
        await message.answer(text="К сожалению, мы не нашли пользователя с таким id.")


@router.callback_query((StateFilter(FSMDeleteUser.finish)), F.data.in_(["delete_user", "cancel_delete"]))
async def delete_user_finish(callback: CallbackQuery, state: FSMContext):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    if callback.data == "delete_user":
        print(await state.get_data())
        user_state_data = await state.get_data()
        delete_user_in_db(role=user_state_data['user_role'], user_id=user_state_data['user_id'])
        await callback.message.answer(text="Пользователь успешно удален")
        await state.clear()
    elif callback.data == "cancel_delete":
        await callback.message.answer(text="Вы отменили удаления пользователя")
        await state.clear()


async def for_admin_message(bot: Bot):
    try:
        clear_offer_data()

        for admin_id in users_list("admins"):
            await bot.send_message(text="INFO:\nЗаявки в БД очищены.", chat_id=str(admin_id))
    except Exception as e:
        print(e)

