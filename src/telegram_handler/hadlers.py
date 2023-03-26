import logging
import os
from pathlib import Path
from uuid import uuid4

from aiogram import types
from PIL import Image

from src.telegram_handler import img_to_code


async def show_hello_handler(message: types.Message):
    await message.answer(
        text=f"Hello, {message.from_user.username}! Send me an image and I will extract code from it!:)")


async def photo_handler(message: types.Message):
    photo_size: types.PhotoSize = message.photo[-1]
    file_info = await message.bot.get_file(photo_size.file_id)
    file_ext = file_info.file_path.split(".")[-1]

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
