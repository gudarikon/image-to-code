import logging
import os

from aiogram import Bot, Dispatcher, executor, types

from src.telegram_handler.handlers import photo_handler, show_hello_handler

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

@dp.message_handler(content_types=["document"])
async def handle_file(message: types.Message):
    file_id = message.document.file_id
    print(dir(message.document))
    print(vars(message.document))
    print(message.document.mime_base)
    logging.debug(dir(message.document))
    logging.debug(vars(message.document))
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await message.answer(text=f"file path is {file_path} :)")
    # await bot.download_file(file_path, "text.txt")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
