import logging
import os

from aiogram import Bot, Dispatcher, executor, types

from .hadlers import photo_handler, show_hello_handler

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def show_hello(message: types.Message):
    await show_hello_handler(message)


@dp.message_handler(content_types=["photo"])
async def handle_photo(message: types.Message):
    await photo_handler(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
