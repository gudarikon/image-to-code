from dataclasses import dataclass
import logging
from unittest.mock import AsyncMock

import pytest

from src.telegram_handler.hadlers import show_hello_handler


@dataclass
class User:
    username: str


@pytest.mark.asyncio
async def test_show_hello():
    name = "masstermax"
    message_mock = AsyncMock(from_user=User(name))
    await show_hello_handler(message=message_mock)
    expected = f"Hello, {name}! Send me an image and I will extract code from it!:)"
    logging.info(message_mock.return_value)
    logging.info(dir(message_mock.return_value))
    logging.info(vars(message_mock.return_value))
    assert expected == message_mock.answer.text
