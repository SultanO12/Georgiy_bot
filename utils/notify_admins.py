import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
        try:
            await dp.bot.send_message(ADMINS[0], "Бот запущен")

        except Exception as err:
            logging.exception(err)
