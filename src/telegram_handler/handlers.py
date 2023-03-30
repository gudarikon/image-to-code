import logging
from pathlib import Path
import tempfile
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
    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_path = Path(tmpdirname)
        file_name = f"{uuid4()}.{file_ext}"
        await photo_size.download(destination_file=dir_path / file_name)
        logging.info(f"downloaded: {file_name}")

        file_path = dir_path / file_name
        logging.info(f"file path: {file_path}")

        image = Image.open(file_path).copy()
    logging.info(image)

    ocr_text, code = img_to_code(image, return_ocr_result=False)

    text = ""
    if ocr_text is not None:
        text = f"ocr text:\n\n`{ocr_text}`\n\n"
    text = f"{text}code:\n\n`{code}`"
    logging.info(text)
    await message.answer(text=text, parse_mode="Markdown", reply=True)


async def document_handler(message: types.Message):
    file_id = message.document.file_id
    if message.document.mime_base != "image":
        await message.answer(text="Sorry, I do not understand you:(", reply=True)
    file = await message.bot.get_file(file_id)
    tg_file_path = file.file_path
    file_ext = tg_file_path.split(".")[-1]

    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_path = Path(tmpdirname)
        file_name = f"{uuid4()}.{file_ext}"
        await message.bot.download_file(tg_file_path, dir_path / file_name)
        logging.info(f"downloaded: {file_name}")

        file_path = dir_path / file_name
        logging.info(f"file path: {file_path}")

        image = Image.open(file_path).copy()
    logging.info(image)

    ocr_text, code = img_to_code(image, return_ocr_result=False)

    text = ""
    if ocr_text is not None:
        text = f"ocr text:\n\n`{ocr_text}`\n\n"
    text = f"{text}code:\n\n`{code}`"
    logging.info(text)
    await message.answer(text=text, parse_mode="Markdown", reply=True)
