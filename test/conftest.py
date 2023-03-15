import json
from pathlib import Path

from dotenv import dotenv_values
from PIL import Image
import pytest


@pytest.fixture(scope="module")
def project_path() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(scope="module")
def env_path(project_path) -> Path:
    return project_path / ".env"


@pytest.fixture(scope="module")
def dataset_parser_config_path() -> Path:
    """
    Path to config for dataset_parser

    :return: Path
    """
    return Path(__file__).parent / "resources" / "dataset_parser_config.json"


@pytest.fixture(scope="module")
def image_path() -> Path:
    """
    Path to the source image
    :return: Path
    """
    return Path(__file__).parent / "resources" / "image.png"


@pytest.fixture(scope="module")
def ocr_example_text_path() -> Path:
    """
    Path to the OCR example corrupted text
    :return: Path
    """
    return Path(__file__).parent / "resources" / "ocr_text_example.txt"


@pytest.fixture(scope="module")
def ocr_example_text(ocr_example_text_path) -> str:
    """
    Gets OCR example corrupted text via path

    :param ocr_example_text_path: Path to text
    :return: text
    """
    with open(ocr_example_text_path, "r") as fr:
        text = fr.read()
    return text


@pytest.fixture(scope="module")
def image(image_path) -> Image:
    """
    Gets PIL.Image object via path

    :param image_path: Path to image
    :return: Image object
    """
    return Image.open(image_path)


@pytest.fixture(scope="module")
def paddleocr_config_path() -> Path:
    """
    Path to PaddleProcessor config
    :return: Path
    """
    return Path(__file__).parent / "resources" / "paddleocr_config.json"


@pytest.fixture(scope="module")
def paddleocr_config(paddleocr_config_path) -> dict:
    """
    PaddleProcessor config by path
    :return: dict with PaddleProcessor configs
    """
    with open(paddleocr_config_path, "r") as fr:
        config = json.load(fr)
    return config


@pytest.fixture(scope="module")
def tesseract_config_path() -> Path:
    """
    Path to TesseractProcessor config
    :return: Path
    """
    return Path(__file__).parent / "resources" / "tesseract_config.json"


@pytest.fixture(scope="module")
def tesseract_config(tesseract_config_path, env_path) -> dict:
    """
    TesseractProcessor config by path
    :return: dict with TesseractProcessor configs
    """
    with open(tesseract_config_path, "r") as fr:
        config = json.load(fr)
        config["path_to_tesseract"] = str(Path(dotenv_values(env_path).get("PATH_TO_TESSERACT", "")))
    return config


@pytest.fixture(scope="module")
def code_t5_config_path() -> Path:
    """
    Path to CodeT5Processor config
    :return: Path
    """
    return Path(__file__).parent / "resources" / "code_t5_config.json"


@pytest.fixture(scope="module")
def code_t5_config(code_t5_config_path) -> dict:
    """
    CodeT5Processor config by path
    :return: dict with CodeT5Processor configs
    """
    with open(code_t5_config_path, "r") as fr:
        config = json.load(fr)
        config["model_bin_path"] = Path(__file__).parent.parent / Path(config["model_bin_path"])
    return config


# Here i add some settings to ignore Tesseract if no .env PATH_TO_TESSERACT provided

def pytest_sessionstart(session):
    """
    Set up Variables which should be skipped in case of
    special value and certain condition

    :param session: Pytest session data object
    :return:
    """
    session.skip_variables = {
        "ocr_name": (
            ["TesseractProcessor"],
            dotenv_values(Path(__file__).parent.parent / ".env").get("PATH_TO_TESSERACT", "") == ""
        )
    }


def pytest_runtest_setup(item):
    """
    The given test will be skipped if it uses variable from skip_variables
    and the skip_variable condition is True

    :param item: Test item object
    :return:
    """
    for key in item.session.skip_variables:
        if item.callspec.params.get(key, "") in item.session.skip_variables[key][0] \
                and item.session.skip_variables[key][1]:
            pytest.skip(item.name)
