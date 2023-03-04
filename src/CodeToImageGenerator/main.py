import json
from math import log10
from pathlib import Path
from typing import List, Tuple

import pyautogui

from src.CodeToImageGenerator.config import create_config, save_to_file
from src.CodeToImageGenerator.main_old import DIGIT_INC, GUTTER_BASE, LEFT_BOUND, \
    LINE_HEIGHT, \
    MAX_SYMBOLS, \
    RIGHT_BOUND, \
    SYMBOL_WIDTH, TOP_BOUND, change_visible_lines_number, \
    change_visible_symbols, move_n_lines_rel, open_file, to_start_line
from src.CodeToImageGenerator.repo_parser import parse_repo

config = create_config()


def save_screenshots(lines_num: int, max_symbols: int):
    pyautogui.screenshot(
        Path(config.screenshot_code_folder) / (str(config.id) + ".png"),
        region=calculate_bounds_updated(lines_num, max_symbols))


def calculate_bounds_updated(lines_num: int, max_symbols: int) -> Tuple[
    float, float, float, float]:
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


def traverse_repo():
    if "repo_files" not in config.__dict__:
        config.repo_files = parse_repo(config.repo_path, config.suffixes)
        config.visited_files = set()
    for key in config.visited_files:
        config.repo_files.pop(key, None)

    change_visible_lines_number(29)

    for file in config.repo_files:
        print(file)
        if config.id > 3000:
            print("Stop")
            break
        change_visible_symbols(MAX_SYMBOLS, config.repo_files[file], should_change=True)
        traverse_file_for_functions(file, config.repo_files[file])
        change_visible_symbols_back(MAX_SYMBOLS, config.repo_files[file])
        pyautogui.sleep(0.1)
        config.visited_files.add(file)
    config.visited_files = list(config.visited_files)

    save_to_file(config.__dict__, "config.json")


def traverse_file_for_functions(file_path: str, total_lines: int):
    open_file(file_path)
    to_start_line()
    functions = get_function_lengths(file_path)

    move_n_lines_rel(30)
    for func, max_symbols in functions:
        # print(length)
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
    # current_func_size = 0
    current_func = []
    for i in range(0, len(lines)):
        line = lines[i]
        current_func.append(line)
        max_symbols = max(max_symbols, len(line))
        if prev_line == "    }\n" and line == "\n":
            res.append((current_func[:-1], max_symbols))
            current_func = []
            # current_func_size = -1
            max_symbols = 0
        # current_func_size += 1
        prev_line = line
    return res


if __name__ == "__main__":
    # pyautogui.sleep(3)
    # pyautogui.moveTo(LEFT_BOUND, BOTTOM_BOUND, 0.1)
    pyautogui.hotkey("alt", "tab")
    pyautogui.sleep(1)
    # change_visible_symbols(MAX_SYMBOLS)
    # pyautogui.sleep(0.2)
    # change_visible_symbols_back(MAX_SYMBOLS)
    traverse_repo()
