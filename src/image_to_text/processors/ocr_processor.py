from abc import ABC, abstractmethod
from PIL import Image


class OCRProcessor(ABC):

    @abstractmethod
    def process_image(self, image: Image, add_spaces: bool = False) -> str:
        pass
