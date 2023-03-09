class Config:
    visible_lines: int  # 29 for main_functions
    visible_symbols: int

    code_folder: str
    screenshot_folder: str
    screenshot_code_folder: str

    id: int  # current id of generated screenshot
    repo_files: dict
    visited_files: set
    repo_path: str
    suffixes: list
    code_search_functions_path: str

    def __init__(self, **entries):
        self.__dict__.update(entries)
