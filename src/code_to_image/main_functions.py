import json
from math import log10
from pathlib import Path
from typing import List, Tuple

import pyautogui

from src.code_to_image.config_builder import ConfigBuilder
from src.code_to_image.main_code_blocks import DIGIT_INC, GUTTER_BASE, LEFT_BOUND, \
    LINE_HEIGHT, \
    MAX_SYMBOLS, \
    RIGHT_BOUND, \
    SYMBOL_WIDTH, TOP_BOUND, assert_empty_folders, change_visible_lines_number, \
    change_visible_symbols, move_n_lines_rel, open_file, to_start_line
from src.code_to_image.repo_parser import parse_repo

config = ConfigBuilder().get_config()


def save_screenshots(lines_num: int, max_symbols: int):
    pyautogui.screenshot(
        Path(config.screenshot_code_folder) / (str(config.id) + ".png"),
        region=calculate_bounds_updated(lines_num, max_symbols))


def calculate_bounds_updated(lines_num: int, max_symbols: int) -> \
        Tuple[float, float, float, float]:
    """
    Calculate bounds of code rectangle
    :return: left, top, width, height of code rectangle
    """
    return RIGHT_BOUND - (MAX_SYMBOLS + 1 - 3) * SYMBOL_WIDTH, \
           TOP_BOUND, \
           (max_symbols + 1 - 4) * SYMBOL_WIDTH, \
           (lines_num if lines_num != -1 else config.visible_lines) * LINE_HEIGHT


def change_visible_symbols_back(num_symbols: int = 30, lines_num: int = 100):
    delta_x = (RIGHT_BOUND - LEFT_BOUND) - log10(lines_num) * DIGIT_INC - GUTTER_BASE - (
            num_symbols + 1) * SYMBOL_WIDTH
    pyautogui.mouseDown(LEFT_BOUND + delta_x, 200, button="left")
    pyautogui.moveRel(-delta_x, 0, 0.1)
    pyautogui.mouseUp(button='left')
    config.visible_symbols = num_symbols


def traverse_repo(number_of_functions: int = 3000):
    assert_empty_folders()
    if "repo_files" not in config.__dict__:
        config.repo_files = parse_repo(config.repo_path, config.suffixes)
        config.visited_files = set()
    for key in config.visited_files:
        config.repo_files.pop(key, None)

    change_visible_lines_number(config.visible_lines)

    for file in config.repo_files:
        if config.id > number_of_functions:
            break
        change_visible_symbols(MAX_SYMBOLS, config.repo_files[file], should_change=True)
        traverse_file_for_functions(file)
        change_visible_symbols_back(MAX_SYMBOLS, config.repo_files[file])
        pyautogui.sleep(0.1)
        config.visited_files.add(file)
    config.visited_files = list(config.visited_files)

    ConfigBuilder().save_to_file()


def traverse_file_for_functions(file_path: str):
    open_file(file_path)
    to_start_line()
    functions = get_function_lengths(file_path)

    move_n_lines_rel(config.visible_lines + 1)
    for func, max_symbols in functions:
        pyautogui.sleep(0.2)
        save_screenshots(len(func), max_symbols)
        save_code_to_file(func)
        move_n_lines_rel(len(func) + 1)
        config.id += 1


def save_code_to_file(code: str):
    with open(Path(config.code_folder) / (str(config.id) + ".json"), 'w') as code_file:
        code_file.write(json.dumps({"code": code, "language": "java"}))


def get_function_lengths(file_path) -> List[tuple]:
    with open(file_path, "r") as file:
        lines = file.readlines()[3:]
    res = []
    max_symbols = 0
    prev_line = ""
    current_func = []
    for i in range(0, len(lines)):
        line = lines[i]
        current_func.append(line)
        max_symbols = max(max_symbols, len(line))
        if prev_line == "    }\n" and line == "\n":
            res.append((current_func[:-1], max_symbols))
            current_func = []
            max_symbols = 0
        prev_line = line
    return res


if __name__ == "__main__":
    pyautogui.hotkey("alt", "tab")
    pyautogui.sleep(1)
    traverse_repo()
