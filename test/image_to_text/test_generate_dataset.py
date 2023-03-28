import os

import pytest

from src.image_to_text.generate_dataset import func_generate_dataset


@pytest.mark.parametrize(
    ("images_folder_path_obj", "ocr_name", "ocr_config_path", "add_spaces"),
    [
        ("images_folder_path", "PaddleProcessor", "paddleocr_config_path", False)
    ]
)
def test_func_generate_dataset(images_folder_path_obj, ocr_name, ocr_config_path, add_spaces, tmp_path, request):
    images_folder_path_obj = request.getfixturevalue(images_folder_path_obj)
    ocr_config_path = request.getfixturevalue(ocr_config_path)

    func_generate_dataset(images_folder_path_obj, tmp_path, ocr_name, ocr_config_path, add_spaces)

    for file in (os.listdir(images_folder_path_obj)):
        file_path = (tmp_path / (file.split(".")[0] + ".txt"))
        assert file_path.exists()
        with open(file_path, encoding="utf-16") as f:
            assert len(f.read().strip()) > 0
