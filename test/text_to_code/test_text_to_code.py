import pytest

from src.text_to_code.text_to_code_processors import *
from src.text_to_code import get_processor, text_to_code
from src.text_to_code.text_to_code import func_text_to_code


@pytest.mark.parametrize(
    ("model_name", "expected_type"),
    [
        ("CodeT5Processor", CodeT5Processor),
        ("DummyProcessor", DummyProcessor)
    ]
)
def test_get_processor(model_name, expected_type):
    assert get_processor(model_name), expected_type


@pytest.mark.parametrize(
    "model_name",
    [
        "CodeT5",
        "",
        "blah"
    ]
)
def test_get_processor_fail(model_name):
    with pytest.raises(AssertionError) as err:
        get_processor(model_name)
        assert "No given processor found" in err.value


@pytest.mark.parametrize(
    ("src_text", "model_name", "model_config"),
    [
        ("ocr_example_text", "CodeT5Processor", "code_t5_config"),
        ("ocr_example_text", "DummyProcessor", "code_t5_config"),
    ]
)
def test_img_to_text(src_text, model_name, model_config, request):
    src_text = request.getfixturevalue(src_text)
    model_config = request.getfixturevalue(model_config)

    text = text_to_code(src_text, model_name, model_config)

    assert type(text) == str
    assert len(text) > 0


@pytest.mark.parametrize(
    ("text_path", "processor_name", "processor_config_path"),
    [
        ("ocr_example_text_path", "DummyProcessor", "code_t5_config_path")
    ]
)
def test_func_text_to_code(text_path, processor_name, processor_config_path, request, capsys):
    text_path = request.getfixturevalue(text_path)
    processor_config_path = request.getfixturevalue(processor_config_path)
    func_text_to_code(text_path, processor_name, processor_config_path)
    printed_text = capsys.readouterr().out

    assert type(printed_text) == str
    assert len(printed_text) > 0


