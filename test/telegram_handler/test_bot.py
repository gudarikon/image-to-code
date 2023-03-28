from dataclasses import dataclass
from pathlib import Path
import shutil
from unittest.mock import AsyncMock

import pytest

from src.telegram_handler.handlers import photo_handler, show_hello_handler


@dataclass
class User:
    username: str


@dataclass
class FileInfoMock:
    file_path: str


class PhotoSizeMock:
    def __init__(self, file_id):
        self.file_id = file_id

    async def download(self, destination_file):
        assert destination_file is not None
        path = Path(self.file_id)
        shutil.copyfile(path, destination_file)


class BotMock:
    async def get_file(self, file_id):
        return FileInfoMock(str(file_id))


@pytest.mark.asyncio
async def test_show_hello_handler():
    name = "masstermax"
    message_mock = AsyncMock(from_user=User(name))
    await show_hello_handler(message=message_mock)
    expected = f"Hello, {name}! Send me an image and I will extract code from it!:)"
    message_mock.answer.assert_called_with(text=expected)


@pytest.mark.asyncio
async def test_photo_handler(image_path):
    message_mock = AsyncMock(photo=[PhotoSizeMock(image_path)], bot=BotMock())
    await photo_handler(message=message_mock)
    result = message_mock.answer.call_args.kwargs["text"]
    assert "ocr text" in result
    assert "code" in result
    assert len(result.split("\n")) > 4
