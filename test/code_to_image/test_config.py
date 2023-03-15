"""
    Test that config is read correctly.
"""
from src.code_to_image.config_builder import ConfigBuilder


def test_config_reading(dataset_parser_config_path):
    config = ConfigBuilder().get_config(str(dataset_parser_config_path))
    assert (config.code_search_functions_path == "test\\resources\\java_test_functions.jsonl")
