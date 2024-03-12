from aiogram import Bot
from aiogram.types import BotCommand


# Создаем асинхронную функцию
async def main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    buyer_menu_commands = [
        BotCommand(command='/help',
                   description='справка по работе бота'),
        BotCommand(command='/commands',
                   description='команды для бота')
    ]

    await bot.set_my_commands(buyer_menu_commands)
