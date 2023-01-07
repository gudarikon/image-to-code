from typing import List, Union

from utils import preprocess_text


def text_to_code(source_text: Union[str, List[str]]):
    source_text = preprocess_text(source_text)
