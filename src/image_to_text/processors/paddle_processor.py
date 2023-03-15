from typing import List

import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

from src import ABCSingleton
from .ocr_processor import OCRProcessor


class PaddleProcessor(OCRProcessor, metaclass=ABCSingleton):
    """
    Class to use PaddleOCR text parser
    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            lang: which language to use while parsing;
        """
        self.lang = kwargs.get("lang", "en")
        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.lang)

    def process_image(self, image: Image, add_spaces: bool = False) -> str:
        """
        Method of image processing

        :param image: source PIL Image object
        :param add_spaces: flag to add spaces for each parsed text row

        :return: Parsed text
        """
        result = self.ocr.ocr(np.array(image), cls=False)[0]
        texts = [line[1][0] for line in result]
        rectangles = [line[0] for line in result]

        if add_spaces:
            spaces = self._process_spaces(rectangles, texts)
            for i, space in enumerate(spaces):
                texts[i] = " " * space + texts[i]

        texts = "\n".join(texts)

        return texts

    def _process_spaces(self, rectangles, texts) -> List[int]:
        """
        Method to get spaces for each row of parsed text

        :param rectangles: list of rectangle coordinates. Ordered like [t-l, t-r, b-r, b-l]
        :param texts: source texts inside of each rectangle
        :return: list of spaces number for each row
        """
        line_widths = [line[1][0] - line[0][0] for line in rectangles]
        average_character_width = [line_widths[i] / len(texts[i]) for i in range(len(texts))]
        average_character_width = sum(average_character_width) / len(average_character_width)

        left_x_border = min(line[0][0] for line in rectangles)
        each_line_shift = [line[0][0] - left_x_border for line in rectangles]
        each_line_spaces_num = [round(line / average_character_width) for line in each_line_shift]

        return each_line_spaces_num
