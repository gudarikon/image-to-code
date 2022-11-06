import json

class Config:
    visible_lines: int
    visible_symbols: int
    code_folder: str
    screenshot_folder: str
    screenshot_code_folder: str
    id: int
    repo_files: dict
    visited_files: set
    repo_path: str
    suffixes: list

    def __init__(self, **entries):
        self.__dict__.update(entries)


def create_config():
    res = Config(**get_file("config.json"))
    res.visited_files = set(res.visited_files)
    return res


def get_file(path: str):
    with open(path, "r") as config_file:
        res = json.loads(config_file.read())
    return res


def save_to_file(info, path: str):
    with open(path, "w") as config_file:
        config_file.write(json.dumps(info))
