from unittest import TestCase

from src.code_to_image.dataset_parser import *


class TestDatasetParser(TestCase):
    """
    Check format of functions file:
    1. function number of lines is not bigger than MAX_LINES (28)
    2. function file is a class to prevent error highlighting
    3. function file ends with line breaks to make possible
    moving caret down for screenshotting last functions
    """

    def test_parsing(self):
        dataset_parser = DatasetParser()
        dataset_parser.config = ConfigBuilder().get_config(
            "../test/resources/dataset_parser_config.json")
        functions = dataset_parser.parse_functions_into_files(functions_num_in_file=29,
                                                              in_memory=True)

        assert (functions.startswith("package edu.hse.ru;\n\nclass Code1 {"))
        assert (functions.endswith("}" + "\n" * 30))

        self._check_functions_are_not_big(functions)

    def _check_functions_are_not_big(self, functions: str):
        line_count = 0
        prev_symbol = ""
        for symbol in functions:
            if symbol == "\n":
                line_count += 1
                if prev_symbol == "\n":
                    assert line_count <= DatasetParser.MAX_LINES
                    line_count = 0
            prev_symbol = symbol
