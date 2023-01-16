from abc import ABC, abstractmethod


class OCRProcessor(ABC):

    @abstractmethod
    def process_image(self, image):
        pass
