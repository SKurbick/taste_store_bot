from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, PhotoSize, BufferedInputFile
from aiogram.filters import Command

from filters.data_validate import IsText, ISPrice, IsPhoto
from lexicon.lexicon import LEXICON_RU, data_translate, help_message, command_role
from keyboards.buyer_keyboard import comm_offer_kb, keyboard_unit, keyboard_yes_no, keyboard_show_my_offers
from keyboards.manager_keyboard import keyboard_order_or_skip

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from states.states import FSMCommOffer
from filters.is_buyer import IsBayerCallback, IsBayerMessage
from utils import add_in_buyer_offers_data, users_list, price_for_manager, show_all_daily_offers

router = Router()

router.message.filter(IsBayerMessage())  # сюда нужно добавить фильтр на весь хендлер модуля
router.callback_query.filter(IsBayerCallback())


# router.startup.register(buyer_menu)


@router.message(Command(commands="buyer"))  # example
async def buyer_handler(message: Message):
    await message.answer(text=LEXICON_RU["/buyer"])
    print(message.from_user.id)


@router.message(Command(commands="start"), StateFilter(default_state))
async def start(message: Message):
    await message.answer(text=LEXICON_RU["/start_buyer"])


@router.message(Command(commands="comm_offer"), StateFilter(default_state))
async def comm_offer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["comm_offer"])

    # устанавливаем ожидание ввода наименования продукта
    await state.set_state(FSMCommOffer.product_name)


@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def cancel_comm_offer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["cancel_comm_offer"])
    await state.clear()


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне состояния формирования заявки'
    )


@router.message(StateFilter(FSMCommOffer.product_name), IsText())
async def product_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Спасибо!\nА теперь отправьте цену за единицу товара (за кг или шт):")

    # устанавливаем ожидание ввода цены
    await state.set_state(FSMCommOffer.price)


@router.message(StateFilter(FSMCommOffer.product_name))
async def wrong_product_name_sent(message: Message):
    await message.answer(text="Вы прислали что-то непохожее на наименование продукта")


@router.message(StateFilter(FSMCommOffer.price), ISPrice())
async def price_sent(message: Message, state: FSMContext):
    await state.update_data(result_price=price_for_manager(message.text))
    await state.update_data(buyer_price=message.text)
    await message.answer(
        text="Супер!\nА теперь укажите это цена за килограмм или штуку:",
        reply_markup=keyboard_unit
    )
    await state.set_state(FSMCommOffer.unit)


@router.message(StateFilter(FSMCommOffer.price))
async def wrong_product_name_sent(message: Message):
    await message.answer(text="Вы прислали что-то непохожее на цену товара")


@router.callback_query(StateFilter(FSMCommOffer.unit), F.data.in_(["thing", "kg"]))
async def unit_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(unit=callback.data)
    # удаляет inline-кнопку
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer(
        text="Отлично!\nА теперь жду фото товара:"
    )

    await state.set_state(FSMCommOffer.upload_photo)


@router.message(StateFilter(FSMCommOffer.upload_photo), F.photo[-1].as_("largest_photo"), IsPhoto())
async def photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
    print(message is list[Message])
    """Обрабатывает полученное фото -> Отвечает обратным сообщением ожидая подтверждение заявки """

    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )

    await message.bot.download(
        message.photo[-1],
        destination=f"buyer_photos/{largest_photo.file_id}.jpg"
    )
    data = await state.get_data()
    await message.answer(text="Отлично!\n Подтвердите вашу заявку:")
    with open(f"buyer_photos/{largest_photo.file_id}.jpg", "rb") as image_from_buffer:
        await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(),
                filename="image.jpg"
            ),
            caption=f"Наименование продукта: {data['name']}\n цена: {data['buyer_price']}руб. за {data_translate[data['unit']]}\n",
            reply_markup=keyboard_yes_no
        )
    await state.set_state(FSMCommOffer.yes_no)


@router.message(StateFilter(FSMCommOffer.upload_photo))
async def photo_sent(message: Message):
    await message.answer(text="Вы прислали что-то непохожее на фото")


@router.callback_query(StateFilter(FSMCommOffer.yes_no), F.data.in_(["yes", "no"]))
async def yes_no_offer_status(callback: CallbackQuery, state: FSMContext):
    """Если YES бот сохраняет заявку в БД в json файле и рассылает заявку со скорректированной ценой
    всем менеджерам из списка"""
    if callback.data == "yes":
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        data = await state.get_data()

        # сохранение заявки в БД
        add_in_buyer_offers_data(
            buyer_id=callback.from_user.id,
            offer_id=callback.message.message_id,
            offer_data=data)

        print(callback.from_user.id, callback.message.message_id)

        # рассылка заяки всем менеджерам
        with open(f"buyer_photos/{data['photo_id']}.jpg", "rb") as image_from_buffer:

            for manager in users_list("managers"):
                await callback.bot.send_photo(
                    chat_id=manager,
                    photo=BufferedInputFile(
                        image_from_buffer.read(),
                        filename="some name",
                    ),
                    caption=f"Наименование продукта: {data['name']}\n цена: {data['result_price']}руб. за {data_translate[data['unit']]}\n",
                    # reply_markup=keyboard_order_or_skip
                )
        await state.clear()
        await callback.message.answer("Отлично!\nЗаявка сформирована.")

    """Если NO """
    if callback.data == "no":
        # удаляет inline-кнопку
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        await state.clear()
        await callback.message.answer(text="Вы отменили формирование заявки.")


@router.message(Command(commands="help"))
async def help_bayer_message(message: Message):
    await message.answer(text=help_message["help_buyer"])


@router.message(Command(commands="commands"))
async def help_bayer_message(message: Message):
    await message.answer(text=command_role["command_buyer"])


@router.message(Command(commands="show_my_offers"))
async def show_my_offers(message: Message):
    print(message.from_user.id)
    if show_all_daily_offers(buyer_id=str(message.from_user.id)):
        await message.answer(
            text="На сегодня у вас есть несколько сформированных предложений.\n Подтвердите ваш запрос:",
            reply_markup=keyboard_show_my_offers)
    else:
        await message.answer(
            text="За этот день от вас еще не было ни одного предложения:(\nОчень ждём!")


@router.callback_query(F.data.in_(["show_my_offers", "cancel_show_offers"]))
async def status_show_offers(callback: CallbackQuery):
    "удаляет кнопки для текущего пользователя"
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    if callback.data == "show_my_offers":
        all_daily_offers = show_all_daily_offers(buyer_id=str(callback.from_user.id))
        if all_daily_offers:
            for offer_id in all_daily_offers:
                for offer_data in offer_id.values():
                    action_message = f"Наименование продукта: {offer_data['name']}\nЦена: {offer_data['buyer_price']} руб. за {data_translate[offer_data['unit']]}\n"
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
