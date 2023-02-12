import pytesseract

from .ocr_processor import OCRProcessor
from src import Singleton


class TesseractProcessor(OCRProcessor, metaclass=Singleton):

    def __init__(self, **kwargs):
        assert kwargs.get("path_to_tesseract", "") != "", "You should pass Tesseract.exe file's path as " \
                                                          "`path_to_tesseract` "
        self.path_to_tesseract = kwargs["path_to_tesseract"]
        pytesseract.pytesseract.tesseract_cmd = self.path_to_tesseract

    def process_image(self, image):
        result = pytesseract.image_to_string(image, config="--psm 4")
        return result
