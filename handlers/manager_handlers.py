from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from keyboards.manager_keyboard import keyboard_show_all_offers
from lexicon.lexicon import LEXICON_RU, help_message, data_translate, command_role
from filters.is_manager import IsManagerCallback, IsManagerMessage
from utils import show_all_daily_offers

router = Router()
router.message.filter(IsManagerMessage())  # место для фильтра на весь модуль
router.callback_query.filter(IsManagerCallback())


@router.callback_query(F.data.in_(["order", "skip"]))
async def order_status(callback: CallbackQuery):
    await callback.message.answer(text="чики брики в менеджеры!!")


@router.message(Command(commands="start"))
async def manager_start(message: Message):
    await message.answer(text=LEXICON_RU["/start_manager"])


@router.message(Command(commands="help"))
async def help_manager_message(message: Message):
    await message.answer(text=help_message["help_manager"])


@router.message(Command(commands="commands"))
async def help_bayer_message(message: Message):
    await message.answer(text=command_role["command_manager"])


@router.message(Command(commands="show_offers"))
async def show_daily_offers(message: Message):
    if len(show_all_daily_offers()) > 0:
        await message.answer(
            text="Есть несколько предложений для вас.\n Подтвердите ваш запрос и мы вышлем вам всё что у нас есть!",
            reply_markup=keyboard_show_all_offers)
    else:
        await message.answer(
            text="К сожалению за день ещё не было сформированно ни одного коммерческого предложения :(")


@router.callback_query(F.data.in_(["show_all_offers", "cancel_show_offers"]))
async def status_show_offers(callback: CallbackQuery):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    if callback.data == "show_all_offers":
        all_daily_offers = show_all_daily_offers()

        for buyer_id in all_daily_offers.values():
            for offer_id in buyer_id:
                for offer_data in offer_id.values():
                    action_message = f"Наименование продукта: {offer_data['name']}\n цена: {offer_data['result_price']} руб. за {data_translate[offer_data['unit']]}\n"
                    with open(f"buyer_photos/{offer_data['photo_id']}.jpg", "rb") as image_from_buffer:
                        await callback.message.answer_photo(
                            BufferedInputFile(
                                image_from_buffer.read(),
                                filename="image.jpg"
                            ),
                            caption=action_message
                        )

    if callback.data == "cancel_show_offers":
        await callback.message.answer(text="Вы отменили действие.")
