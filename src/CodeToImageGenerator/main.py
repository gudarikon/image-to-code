import json
from math import log10
from pathlib import Path
import platform
import random
from time import sleep
from typing import List, Tuple

import pyautogui

from config import create_config, save_to_file
from repo_parser import get_language, parse_repo

DIGIT_INC = 9.5
GUTTER_BASE = 35

MAX_SYMBOLS = 160  # 177
MIN_SYMBOLS = 10
SYMBOL_WIDTH = 10
LINE_HEIGHT = 27.5

TOP_BOUND = 106
BOTTOM_BOUND = 940
RIGHT_BOUND = 1895  # 26
LEFT_BOUND = 64

spaces_in_tab = 4
config = create_config()


def open_file(path: str):
    if platform.system == "Darwin":
        pyautogui.hotkey("cmd", "shift", "o")
    else:
        pyautogui.hotkey("ctrl", "shift", "n")
    pyautogui.typewrite(path, interval=0.05)
    pyautogui.hotkey("enter")
    sleep(0.5)


def to_start_line():
    """
    Move caret to `line_number`, that will be displayed as the top line of visible code.
    1. Move to (`line_number` + `visible_lines_number`) number
    2. Move caret (`visible_lines_number` - 1) up. That way `line_number` will be the topmost line
    """
    # scroll is unreliable because it is different from time to time
    pyautogui.hotkey("ctrl", "home")


def move_n_lines_rel(lines_number: int):
    """
    Move n lines down from this relative position
    :param lines_number: number of moved lines
    """
    for _ in range(lines_number):
        pyautogui.hotkey("down")


def change_visible_lines_number(num_lines=30):
    """
    Changing visible lines number is achieved by moving terminal window up.
    :param num_lines: number of lines that will be visible after. Maximal value is 30.
    """
    if config.visible_lines == -1:
        pyautogui.mouseDown(x=400, y=BOTTOM_BOUND, button='left')
    else:
        pyautogui.mouseDown(x=400, y=config.visible_lines * LINE_HEIGHT + TOP_BOUND, button='left')
    pyautogui.moveTo(400, TOP_BOUND, 0.1)
    pyautogui.moveTo(400, TOP_BOUND + LINE_HEIGHT * num_lines, 0.1)
    pyautogui.mouseUp(button='left')
    config.visible_lines = num_lines


def save_screenshots(lines_num: int):
    pyautogui.screenshot(Path(config.screenshot_folder) / (str(config.id) + ".png"))
    pyautogui.screenshot(Path(config.screenshot_code_folder) / (str(config.id) + ".png"),
                         region=calculate_bounds(lines_num))


def save_file(file_path: str, total_lines: int):
    """
    Parse file into screenshots and text from these screens
    :param file_path: path to parsed file
    :param total_lines: lines in that file
    """
    open_file(file_path)
    to_start_line()
    with open(file_path, 'r') as traversed_file:
        caret_line = 1
        lines = traversed_file.readlines()
        stops = create_random_screen_stops(total_lines)

        for i, stop in enumerate(stops):
            if i == 0:
                move_n_lines_rel(stop - caret_line + config.visible_lines - 2)
            else:
                move_n_lines_rel(stop - caret_line)
            caret_line = stop
            print(caret_line)
            sleep(1)
            text, is_trimmed = process_text(lines[stop - 1:stop + config.visible_lines - 1])
            if not is_trimmed:
                with open(Path(config.code_folder) / (str(config.id) + ".json"),
                          'w') as code_file:
                    code_file.write(
                        json.dumps({"code": text, "language": get_language(file_path)}))
                save_screenshots(total_lines)
                config.id += 1


def create_random_screen_stops(total_lines: int):
    """
    Create random lines where screenshot will be taken
    :param total_lines: lines in file
    """
    res = []
    current = random.randint(1, config.visible_lines)
    while current + config.visible_lines < total_lines:
        res.append(current)
        current += random.randint(config.visible_lines, 2 * config.visible_lines)
    print(res[:len(res) - 1])
    return res[:len(res) - 1]


def process_text(lines: List[str]) -> tuple:
    """
    Replace tabs with spaces, convert list to string
    :param lines: list of processed lines
    :return: and bool for trimmed symbols
    """
    res = []
    is_trimmed = False
    for line in lines:
        no_tabs = line.replace("\t", " " * spaces_in_tab)[:len(line) - 1]
        if len(no_tabs) >= config.visible_symbols:
            is_trimmed = True
        res.append(no_tabs)
    return res, is_trimmed


def change_visible_symbols(num_symbols: int = 30, lines_num: int = 100):
    if config.visible_symbols == -1:
        pyautogui.mouseDown(LEFT_BOUND, 200, button="left")
        pyautogui.moveRel(
            (RIGHT_BOUND - LEFT_BOUND)  # move from right to left
            - log10(lines_num) * DIGIT_INC - GUTTER_BASE  # not counting gutter
            - (num_symbols + 1) * SYMBOL_WIDTH, 0, 0.1)  # not counting num_symbols
        pyautogui.mouseUp(button='left')
        config.visible_symbols = num_symbols
        #


def calculate_bounds(lines_num: int) -> Tuple[float, float, float, float]:
    """
    Calculate bounds of code rectangle
    :return: left, top, width, height of code rectangle
    """
    return RIGHT_BOUND - (config.visible_symbols + 1) * SYMBOL_WIDTH, \
           TOP_BOUND, \
           (config.visible_symbols + 1) * SYMBOL_WIDTH, \
           config.visible_lines * LINE_HEIGHT


def traverse_file(file_path: str, total_lines: int):
    change_visible_lines_number(random.randint(10, 28))
    x, y = pyautogui.position()
    save_file(file_path, total_lines)
    return x, y


def traverse_repo():
    if "repo_files" not in config.__dict__:
        config.repo_files = parse_repo(config.repo_path, config.suffixes)
        config.visited_files = set()
    for key in config.visited_files:
        config.repo_files.pop(key, None)
    for file in config.repo_files:
        change_visible_symbols(MAX_SYMBOLS, config.repo_files[file])
        x, y = traverse_file(file, config.repo_files[file])
        config.visited_files.add(file)
        newx, newy = pyautogui.position()
        if abs(x - newx) > 10 or abs(y - newy) > 10:
            config.visited_files = list(config.visited_files)
            save_to_file(config.__dict__, "config.json")
            return
    config.visited_files = list(config.visited_files)
    save_to_file(config.__dict__, "config.json")


if __name__ == "__main__":
    traverse_repo()
