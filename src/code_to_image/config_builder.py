import json

from .config import Config


class ConfigBuilderMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def get_file(path: str):
    with open(path, "r") as config_file:
        res = json.loads(config_file.read())
    return res


def create_config():
    res = Config(**get_file("config.json"))
    res.visited_files = set(res.visited_files)
    return res


class ConfigBuilder(metaclass=ConfigBuilderMeta):
    current_config = create_config()
    """
    Singleton for changing and getting Config
    """

    def get_config(self) -> Config:
        pass

    def update_repo_path(self, repo_path: str):
        self.current_config.repo_path = repo_path
        return self

    def update_folders(self,
                       code_folder: str = None,
                       screenshot_folder: str = None,
                       screenshot_code_folder: str = None):
        if code_folder is not None:
            self.current_config.code_folder = code_folder
        if screenshot_folder is not None:
            self.current_config.screenshot_folder = screenshot_folder
        if screenshot_code_folder is not None:
            self.current_config.screenshot_code_folder = screenshot_code_folder
        return self

    def update_code_search_functions_path(self, path: str):
        self.current_config.code_search_functions_path = path
        return self

    def save_to_file(self, path: str = "config.json"):
        with open(path, "w") as config_file:
            config_file.write(json.dumps(self.current_config.__dict__))
