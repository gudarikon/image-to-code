from typing import List, Union


def preprocess_text(source_text: Union[str, List[str]]):
    if isinstance(source_text, list):
        source_text = "\n".join([s.lstrip() for s in source_text if not s.isspace() and len(s) > 0])
    return source_text
