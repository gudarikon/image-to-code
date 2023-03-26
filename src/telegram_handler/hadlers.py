
# TODO read https://github.com/aiogram/aiogram/issues/378


async def show_hello_handler(message):
     await message.answer(
        text=f"Hello, {message.from_user.username}! Send me an image and I will extract code from it!:)")


async def photo_handler(message):
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
