import numpy as np
from paddleocr import PaddleOCR

from .ocr_processor import OCRProcessor
from src import Singleton


class PaddleProcessor(OCRProcessor, metaclass=Singleton):

    def __init__(self, **kwargs):
        self.lang = kwargs.get("lang", "en")
        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.lang)

    def process_image(self, image):
        result = self.ocr.ocr(np.array(image), cls=False)[0]
        texts = [line[1][0] for line in result]
        texts = "\n".join(texts)
        return texts
