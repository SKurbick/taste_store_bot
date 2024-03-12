from pprint import pprint

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdminMessage(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


class IsPhoneNumber(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        if message.text:
            if message.text.isdigit() and len(message.text) == 11:
                return True
            else:
                return False
        else:
            return False


class IsUserName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            if ' ' in message.text.strip() and message.text.count(' ') == 1:
                user_name = message.text.strip(" ")
                if user_name[0].isalpha() and user_name[1].isalpha():
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False


class IsText(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            if message.text.isalpha():
                return True


class ISPrice(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            if message.text.isdigit():
                return True


class IsPhoto(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.photo:
            return True


class IsUserID(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            if message.text.isdigit():
                return True
