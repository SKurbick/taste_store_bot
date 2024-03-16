import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import admin_handlers, manager_handlers, buyer_handlers, registration_handlers
from config_data import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.admin_handlers import for_admin_message
from menu.main_menu import main_menu
from middleware.middleware import GetAlbum

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)


async def main() -> None:
    config: Config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info("STARTING BOT")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(for_admin_message, 'cron', hour=13, minute=11, args=(bot,), timezone='Europe/Moscow')

    dp.include_router(registration_handlers.router)

    dp.include_router(admin_handlers.router)
    dp.include_router(manager_handlers.router)
    dp.include_router(buyer_handlers.router)
    dp.startup.register(main_menu)
    dp.message.outer_middleware(GetAlbum())
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# TODO: добавить в форму заявки пункт "место происхождения"
