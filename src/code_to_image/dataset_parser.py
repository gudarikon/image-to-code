from io import StringIO
import json
from typing import TextIO

from .config_builder import ConfigBuilder
from .main_code_blocks import MAX_SYMBOLS


class DatasetParser:
    config = ConfigBuilder().get_config()
    # maximum lines in function to make it possible to screenshot
    MAX_LINES = 28
    current_file_num = 1

    def create_file(self, in_memory: bool = False) -> TextIO:

        res = StringIO() if in_memory else open(
            self.config.repo_path + f"\\Code{self.current_file_num}.java",
            "w",
            encoding="ascii"
        )
        res.write("package edu.hse.ru;\n\n")
        res.write(f"class Code{self.current_file_num} ")
        res.write("{\n")

        self.current_file_num += 1
        return res

    def write_code_if_fit(self, code: str, file: TextIO):
        if code.count("\n") + 1 > self.MAX_LINES:
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

    def parse_functions_into_files(self, functions_num_in_file: int = 100, in_memory: bool = False):
        with open(self.config.code_search_functions_path, 'r') as json_file:
            json_list = list(json_file)

        i = 0
        write_file = self.create_file(in_memory)
        for json_str in json_list:
            if i == functions_num_in_file:
                write_file.write("}")
                write_file.write(
                    "\n" * 30)  # make empty lines at the end to screenshot last functions
                if in_memory:
                    return write_file.getvalue()
                write_file = self.create_file(in_memory)
                i = 0
            result = json.loads(json_str)
            self.write_code_if_fit(result["code"], write_file)
            i += 1
        write_file.write("}")


if __name__ == "__main__":
    parser = DatasetParser()
    parser.parse_functions_into_files()
