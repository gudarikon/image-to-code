from .data_processor import DataProcessor


class CodeT5DataProcessor(DataProcessor):

    def __init__(self):
        pass

    def process(self, text, **kwargs):
        if isinstance(text, list):
            text = "\n".join([s.lstrip() for s in text if not s.isspace() and len(s) > 0])
        return text
