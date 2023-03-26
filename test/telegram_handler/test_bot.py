from dataclasses import dataclass
import os
from unittest.mock import AsyncMock

import pytest

from src.telegram_handler.hadlers import photo_handler, show_hello_handler


@dataclass
class User:
    username: str


@dataclass
class FileInfoMock:
    file_path: str


class PhotoSizeMock:
    def __init__(self, file_id):
        self.file_id = file_id
        assert "." in file_id

    async def download(self):
        # use with . in tests
        assert self.file_id in os.listdir('.')


class BotMock:
    async def get_file(self, file_id):
        return FileInfoMock(file_id)


@pytest.mark.asyncio
async def test_show_hello_handler():
    name = "masstermax"
    message_mock = AsyncMock(from_user=User(name))
    await show_hello_handler(message=message_mock)
    expected = f"Hello, {name}! Send me an image and I will extract code from it!:)"
    message_mock.answer.assert_called_with(text=expected)


@pytest.mark.asyncio
async def test_photo_handler():
    message_mock = AsyncMock(photo=[PhotoSizeMock("test_img.png")], bot=BotMock())
    await photo_handler(message=message_mock)
    message_mock.answer.assert_called_with(text="123")
