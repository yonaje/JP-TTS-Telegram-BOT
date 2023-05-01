import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import character_related_commands, commands
from data.config import TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(character_related_commands.router, commands.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
