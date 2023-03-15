from src.text_to_code.utils import preprocess_text
from .data_processor import DataProcessor


class CodeT5DataProcessor(DataProcessor):

    def __init__(self):
        pass

    def process(self, text, **kwargs):
        return preprocess_text(text, strip_lines=True)
