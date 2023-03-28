"""
Test that:
1. crop_image correctly crops one line off, where the horizontal scrollbar should be
2. crop_code removes one last line
"""
import json
from math import floor
from typing import List

from PIL import Image

from src.code_to_image.crop import crop_code, crop_image
from src.code_to_image.main_code_blocks import LINE_HEIGHT


def test_crop_image(image_path, tmp_path):
    json_id = 1
    crop_image(str(image_path), json_id, str(tmp_path))

    image_height = Image.open(image_path).size[1]
    cropped_image_height = Image.open(tmp_path / (str(json_id) + ".png")).size[1]

    assert image_height == cropped_image_height + floor(LINE_HEIGHT)


def test_crop_code(code_path, resources_path):
    json_id = 1
    crop_code(str(code_path), json_id, str(resources_path))

    code = _get_code(str(code_path))
    cropped_code = _get_code(str(resources_path / (str(json_id) + ".json")))

    assert len(code) == len(cropped_code) + 1
    for i, line in enumerate(cropped_code):
        assert line == code[i]


def _get_code(path: str) -> List[str]:
    with open(path, 'r') as file:
        json_file = json.loads(file.read())
        return json_file['code']
