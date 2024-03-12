from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils import users_list


class IsRegUsersMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        all_users = [*users_list("managers"), *users_list("admins"), *users_list("buyers")]

        return message.from_user.id in all_users
