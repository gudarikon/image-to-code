from typing import List, Union


def preprocess_text(source_text: Union[str, List[str]]):
    if isinstance(source_text, list):
        source_text = "\n".join(source_text)
    return source_text
