import json
from typing import TextIO

from src.code_to_image.main_old import MAX_SYMBOLS

REPO_PATH = "C:\\Users\\alex\\Documents\\GitHub\\dataset_image_to_code\\src\\edu\\hse\\ru"
JSONL_PATH = "C:\\Users\\alex\\Desktop\\java_test_0.jsonl"
# maximum lines in function to make it possible to screenshot
MAX_LINES = 28
current_file_num = 1


def create_file() -> TextIO:
    global current_file_num

    res = open(REPO_PATH + "\\Code{num}.java".format(num=current_file_num), "w", encoding="ascii")
    res.write("package edu.hse.ru;\n\n")
    res.write("class Code{num} ".format(num=current_file_num))
    res.write("{\n")

    current_file_num += 1
    return res


def write_code_if_fit(code: str, file: TextIO):
    if code.find("void addOrder(String condition) {") != -1:
        print(code)
    if code.find("public FullEntity<?> save(final P pojo, final SaveContext ctx) {") != -1:
        print(code)
    if code.count("\n") + 1 > MAX_LINES:
        return
    lines = code.split("\r\n") if code.find("\r\n") != -1 else code.split("\n")
    if len(list(filter(lambda x: len(x) > (MAX_SYMBOLS - 1), lines))) > 0:
        return
    try:
        code.encode(encoding="ascii")
        file.write("\n".join(lines))
        file.write("\n\n")
    except UnicodeEncodeError as e:
        print(code)
        return


if __name__ == "__main__":
    with open(JSONL_PATH, 'r') as json_file:
        json_list = list(json_file)

    i = 0
    # files_num = 0
    write_file = create_file()
    for json_str in json_list:
        if i == 100:
            #  files_num += 1
            # if files_num == 10:
            #     break
            write_file.write("}")
            write_file.write("\n" * 30)
            write_file = create_file()
            i = 0
        result = json.loads(json_str)
        write_code_if_fit(result["code"], write_file)
        i += 1
    write_file.write("}")
