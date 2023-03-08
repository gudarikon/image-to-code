import os
import logging

from aiogram import Bot, Dispatcher, executor, types


BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')


logging.basicConfig(level=logging.INFO)
logging.info(BOT_API_TOKEN)


bot = Bot(BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def show_weather(message: types.Message):
    await message.answer(text="hello!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
