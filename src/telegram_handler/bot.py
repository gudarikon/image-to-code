import logging
import os
from pathlib import Path
from uuid import uuid4

from aiogram import Bot, Dispatcher, executor, types
from PIL import Image

from pipeline_manager import img_to_code

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def show_hello(message: types.Message):
    await message.answer(text=f"Hello world from {message.from_user.username}!")


@dp.message_handler(content_types=["photo"])
async def handle_photo(message):
    photo_size: types.PhotoSize = message.photo[-1]
    file_info = await bot.get_file(photo_size.file_id)
    file_ext = file_info.file_path.split(".")[-1]
    # todo which name prefer?
    # file_name = f"{photo_size.file_unique_id}.{file_ext}"
    file_name = f"{uuid4()}.{file_ext}"
    await message.photo[-1].download(file_name)
    logging.info(f"downloaded: {file_name}")

    file_path = Path(file_name)
    logging.info(f"file path: {file_path}")

    image = Image.open(file_path)
    logging.info(image)

    ocr_text, code = img_to_code(image, return_ocr_result=True)

    text = "\n\n".join(["ocr text:", f"`{ocr_text}`", "code:", f"`{code}`"])
    logging.info(text)
    await message.answer(text=text, parse_mode="Markdown", reply=True)

    # delete image
    try:
        os.remove(file_path)
    except FileNotFoundError:
        logging.warning(f"file to delete was not found: {file_path}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
