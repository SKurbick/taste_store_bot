from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from utils.utils import users_list


class IsAdminCallback(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.from_user.id in users_list("admins")


class IsAdminMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in users_list("admins")
