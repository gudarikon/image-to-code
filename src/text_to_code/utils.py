from typing import List, Union


def preprocess_text(source_text: Union[str, List[str]], strip_lines: bool = True) -> str:
    if isinstance(source_text, str):
        source_text = ["\n" + s for s in source_text.split("\n")]
        source_text[0] = source_text[0][1:]
    if strip_lines:
        source_text = "\n".join([s.lstrip() for s in source_text if not s.isspace() and len(s) > 0])
    else:
        source_text = "".join([s for s in source_text if not s.isspace() and len(s) > 0])
    return source_text
