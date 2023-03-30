import pytest

from src.telegram_handler import img_to_code
from src.telegram_handler.pipeline_manager import func_img_to_code


@pytest.mark.parametrize(
    ("src_image", "ocr_name", "ocr_config", "text_to_code_processor", "processor_config", "return_ocr_result"),
    [
        ("image", "PaddleProcessor", None, "CodeT5Processor", None, True),
        ("image", "TesseractProcessor", "tesseract_config", "DummyProcessor", "code_t5_config", False)
    ]
)
def test_img_to_code(
        src_image,
        ocr_name,
        ocr_config,
        text_to_code_processor,
        processor_config,
        return_ocr_result,
        request
):
    src_image = request.getfixturevalue(src_image)
    if ocr_config is not None:
        ocr_config = request.getfixturevalue(ocr_config)
    if processor_config is not None:
        processor_config = request.getfixturevalue(processor_config)

    text = img_to_code(
        src_image,
        ocr_name,
        ocr_config,
        text_to_code_processor,
        processor_config,
        return_ocr_result
    )

    ocr_text, text = text
    if return_ocr_result:
        assert type(ocr_text) == str
        assert len(ocr_text) > 0
    assert type(text) == str
    assert len(text) > 0


def test_func_image_to_code(image_path, capsys):
    func_img_to_code(image_path)

    printed_text = capsys.readouterr().out

    assert type(printed_text) == str
    assert len(printed_text) > 0
