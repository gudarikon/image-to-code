from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from src.telegram_handler.hadlers import show_hello_handler


@dataclass
class User:
    name: str


@pytest.mark.asyncio
async def test_show_hello():
    name = "masstermax"
    message_mock = AsyncMock(from_user=User(name))
    await show_hello_handler(message=message_mock)
    message_mock.answer.assert_called_with(f"Hello, {name}! Send me an image and I will extract code from it!:)")