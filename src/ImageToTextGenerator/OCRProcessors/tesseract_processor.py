import numpy as np
from paddleocr import PaddleOCR
import pytesseract

from .ocr_processor import OCRProcessor


class TesseractProcessor(OCRProcessor):

    def __init__(self, **kwargs):
        assert kwargs.get("path_to_tesseract", "") != "", "You should pass Tesseract.exe file's path as " \
                                                          "`path_to_tesseract` "
        self.path_to_tesseract = kwargs["path_to_tesseract"]
        pytesseract.pytesseract.tesseract_cmd = self.path_to_tesseract

        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.lang)

    def process_image(self, image):
        result = self.ocr.ocr(np.array(image), cls=False)[0]
        texts = [line[1][0] for line in result]
        texts = "\n".join(texts)
        return texts
