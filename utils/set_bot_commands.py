from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запуск бота"),
            types.BotCommand("menu", "🔻Меню"),
            types.BotCommand("help", "Помощь"),
        ]
    )
