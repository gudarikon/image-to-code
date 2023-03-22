import pytest

from src.image_to_text.processors import *
from src.image_to_text import get_processor, img_to_text


@pytest.mark.parametrize(
    ("ocr_name", "expected_type"),
    [
        ("PaddleProcessor", PaddleProcessor),
        ("TesseractProcessor", TesseractProcessor)
    ]
)
def test_get_processor(ocr_name, expected_type):
    assert get_processor(ocr_name), expected_type


@pytest.mark.parametrize(
    "ocr_name",
    [
        "Paddle",
        "",
        "blah"
    ]
)
def test_get_processor_fail(ocr_name):
    with pytest.raises(AssertionError) as err:
        get_processor(ocr_name)
        assert "No given processor found" in err.value


@pytest.mark.parametrize(
    ("image_obj", "ocr_name", "ocr_config", "add_spaces"),
    [
        ("image", "PaddleProcessor", "paddleocr_config", False),
        ("image", "PaddleProcessor", "paddleocr_config", True),
        ("image", "TesseractProcessor", "tesseract_config", False),
        ("image", "TesseractProcessor", "tesseract_config", True),
    ]
)
def test_img_to_text(image_obj, ocr_name, ocr_config, add_spaces, request):
    image = request.getfixturevalue(image_obj)
    ocr_config = request.getfixturevalue(ocr_config)

    text = img_to_text(image, ocr_name, ocr_config, add_spaces)

    assert type(text) == str
    assert len(text) > 0
