from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from utils import users_list


class IsBayerCallback(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        buyers = users_list("buyers")
        return callback.from_user.id in buyers


class IsBayerMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        buyers = users_list("buyers")

        return message.from_user.id in buyers
