from dataclasses import dataclass
import logging
import os
from pathlib import Path
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
    def __init__(self, file_id, project_path):
        self.file_id = file_id
        self.project_path = project_path

    async def download(self, new_name):
        assert new_name is not None
        path = Path(self.file_id)
        logging.info(f"will mock-download to {self.project_path / new_name}")
        os.popen(f'cp {path} {self.project_path / new_name}')


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
async def test_photo_handler(request):
    image_path = request.getfixturevalue("image_path")
    project_path = request.getfixturevalue("project_path")
    message_mock = AsyncMock(photo=[PhotoSizeMock(image_path, project_path)], bot=BotMock())
    await photo_handler(message=message_mock)
    message_mock.answer.assert_called_with(text="123")
