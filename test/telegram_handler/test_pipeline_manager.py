import pytest

from src.telegram_handler.pipeline_manager import img_to_code


@pytest.mark.parametrize(
    ("src_image", "ocr_processor", "ocr_config", "text_to_code_processor", "processor_config", "return_ocr_result"),
    [
        ("image", "PaddleProcessor", None, "CodeT5Processor", None, True),
        ("image", "TesseractProcessor", "tesseract_config", "DummyProcessor", "code_t5_config", False)
    ]
)
def test_img_to_code(
        src_image,
        ocr_processor,
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
        ocr_processor,
        ocr_config,
        text_to_code_processor,
        processor_config,
        return_ocr_result
    )

    if return_ocr_result:
        text, ocr_text = text
        assert type(ocr_text) == str
        assert len(ocr_text) > 0
    assert type(text) == str
    assert len(text) > 0


