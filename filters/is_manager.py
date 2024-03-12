from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from utils import users_list


class IsManagerCallback(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        managers = users_list("managers")

        return callback.from_user.id in managers


class IsManagerMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        managers = users_list("managers")

        return message.from_user.id in managers
