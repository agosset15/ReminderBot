import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import register_models
from aiogram import Dispatcher
from .config import bot
from .send import router, sendadd


async def main():
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    print('Запускаю БД...')
    register_models()
    print('Запускаю шедулер...')
    scheduler.start()
    scheduler.add_job(sendadd, 'cron', second=0)
    print('Запускаю бота...')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
