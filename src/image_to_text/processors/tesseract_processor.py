from PIL import Image
import pytesseract

from .ocr_processor import OCRProcessor
from src import ABCSingleton


class TesseractProcessor(OCRProcessor, metaclass=ABCSingleton):
    """
    Class to use TesseractOCR text parser
    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            path_to_tesseract - path to Tesseract.exe file
        """
        assert kwargs.get("path_to_tesseract", "") != "", "You should pass Tesseract.exe file's path as " \
                                                          "`path_to_tesseract` "
        self.path_to_tesseract = kwargs["path_to_tesseract"]
        pytesseract.pytesseract.tesseract_cmd = self.path_to_tesseract

    def process_image(self, image: Image, add_spaces: bool = False):
        """
            Method of image processing

            :param image: source PIL Image object
            :param add_spaces: flag to add spaces for each parsed text row

            :return: Parsed text
        """
        result = pytesseract.image_to_string(image, config="--psm 4")
        return result, []
