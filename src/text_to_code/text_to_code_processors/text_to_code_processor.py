from abc import ABC, abstractmethod
from typing import List, Union


class TextToCodeProcessor(ABC):

    @abstractmethod
    def predict(self, text: Union[str, List[str]], **kwargs) -> str:
        pass
