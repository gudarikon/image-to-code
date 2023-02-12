from typing import List, Union

from .text_to_code_processor import TextToCodeProcessor
from src import Singleton


class DummyProcessor(TextToCodeProcessor, metaclass=Singleton):
    def __init__(self, **kwargs):
        """
        Processor that does nothing
        """
        pass

    def predict(self, text: Union[str, List[str]], **kwargs) -> str:
        """
        Just passes text
        :param text: input text
        :return: same text
        """
        if text is list:
            return text.join("\n")
        return text
