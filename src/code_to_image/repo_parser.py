import os
from pathlib import Path


def parse_repo(repo_root: str, suffixes):
    res = {}
    path = os.walk(repo_root)
    for root, _, files in path:
        root = Path(root)
        for file in files:
            if is_suitable_file(file, suffixes):
                with open(str(root / file), 'rb') as fp:
                    c_generator = _count_generator(fp.raw.read)
                    count = sum(buffer.count(b'\n') for buffer in c_generator)
                    res[str(root / file)] = count + 1
    return res


def is_suitable_file(file_name: str, suffixes: list) -> bool:
    for suffix in suffixes:
        if file_name.endswith(suffix):
            return True
    return False


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def get_language(file_path: str):
    ending = file_path.split(".")[-1]
    extensions = {
        "java": "java",
        "py": "python",
        "kt": "kotlin",
        "c": "c",
        "cpp": "c++",
        "go": "go",
        "rs": "rust"
    }
    return extensions.get(ending, "None")
