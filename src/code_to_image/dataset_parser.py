import json
from typing import TextIO

from .config_builder import ConfigBuilder
from .main_old import MAX_SYMBOLS

config = ConfigBuilder().get_config()
# maximum lines in function to make it possible to screenshot
MAX_LINES = 28
current_file_num = 1


def create_file() -> TextIO:
    global current_file_num

    res = open(config.repo_path + "\\Code{num}.java".format(num=current_file_num),
               "w", encoding="ascii")
    res.write("package edu.hse.ru;\n\n")
    res.write("class Code{num} ".format(num=current_file_num))
    res.write("{\n")

    current_file_num += 1
    return res


def write_code_if_fit(code: str, file: TextIO):
    if code.count("\n") + 1 > MAX_LINES:
        return
    lines = code.split("\r\n") if code.find("\r\n") != -1 else code.split("\n")
    if len(list(filter(lambda x: len(x) > (MAX_SYMBOLS - 1), lines))) > 0:
        return
    try:
        code.encode(encoding="ascii")
        file.write("\n".join(lines))
        file.write("\n\n")
    except UnicodeEncodeError:
        return


def parse_functions_into_files(files_num: int = 100):
    with open(config.code_search_functions_path, 'r') as json_file:
        json_list = list(json_file)

    i = 0
    write_file = create_file()
    for json_str in json_list:
        if i == files_num:
            write_file.write("}")
            write_file.write("\n" * 30)  # make empty lines at the end to screenshot last functions
            write_file = create_file()
            i = 0
        result = json.loads(json_str)
        write_code_if_fit(result["code"], write_file)
        i += 1
    write_file.write("}")


if __name__ == "__main__":
    parse_functions_into_files()
