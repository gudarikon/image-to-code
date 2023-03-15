import pytest

from src.text_to_code.utils import preprocess_text


@pytest.mark.parametrize(
    ("source_text", "target_text", "strip_lines"),
    [
        (
            "line1:\n    line2\n    line3\n\n    line4\nline5\n\t\n \nline6",
            "line1:\nline2\nline3\nline4\nline5\nline6",
            True
        ),
        (
            [
                "line1:",
                "    line2",
                "    line3",
                "\n",
                "\n    line4",
                "\nline5",
                "\n\t",
                "\n ",
                "\nline6"
            ],
            "line1:\nline2\nline3\nline4\nline5\nline6",
            True
        ),
(
            "line1:\n    line2\n    line3\n\n    line4\nline5\n\t\n \nline6",
            "line1:\n    line2\n    line3\n    line4\nline5\nline6",
            False
        ),
        (
            [
                "line1:",
                "\n    line2",
                "\n    line3",
                "\n",
                "\n    line4",
                "\nline5",
                "\n\t",
                "\n ",
                "\nline6"
            ],
            "line1:\n    line2\n    line3\n    line4\nline5\nline6",
            False
        )
    ]
)
def test_prepare_image(source_text, target_text, strip_lines):
    processed_text = preprocess_text(source_text, strip_lines)
    assert processed_text == target_text
