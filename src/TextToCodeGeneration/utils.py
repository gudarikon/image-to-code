from typing import List, Union
import re


def preprocess_text(source_text: Union[str, List[str]]):
    if isinstance(source_text, list):
        source_text = " ".join(source_text)
    return re.sub("[ \n\t]+", " ", source_text)
