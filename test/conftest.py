import json
from pathlib import Path

from dotenv import dotenv_values
from PIL import Image
import pytest


@pytest.fixture(scope="module")
def project_path():
    return Path(__file__).parent.parent


@pytest.fixture(scope="module")
def env_path(project_path):
    return project_path / ".env"


@pytest.fixture(scope="module")
def dataset_parser_config_path():
    """
    Path to config for dataset_parser

    :return: Path
    """
    return Path(__file__).parent / "resources" / "dataset_parser_config.json"


@pytest.fixture(scope="module")
def image_path():
    """
    Path to the source image
    :return: Path
    """
    return Path(__file__).parent / "resources" / "image.png"


@pytest.fixture(scope="module")
def image(image_path) -> Image:
    """
    Gets PIL.Image object via path

    :param image_path: Path to image
    :return: Image object
    """
    return Image.open(image_path)


@pytest.fixture(scope="module")
def paddleocr_config_path():
    """
    Path to PaddleProcessor config
    :return: Path
    """
    return Path(__file__).parent / "resources" / "paddleocr_config.json"


@pytest.fixture(scope="module")
def paddleocr_config(paddleocr_config_path):
    """
    PaddleProcessor config by path
    :return: dict with PaddleProcessor configs
    """
    with open(paddleocr_config_path, "r") as fr:
        config = json.load(fr)
    return config


@pytest.fixture(scope="module")
def tesseract_config_path():
    """
    Path to TesseractProcessor config
    :return: Path
    """
    return Path(__file__).parent / "resources" / "tesseract_config.json"


@pytest.fixture(scope="module")
def tesseract_config(tesseract_config_path, env_path):
    """
    TesseractProcessor config by path
    :return: dict with TesseractProcessor configs
    """
    with open(tesseract_config_path, "r") as fr:
        config = json.load(fr)
        config["path_to_tesseract"] = str(Path(dotenv_values(env_path)["PATH_TO_TESSERACT"]))
    return config


@pytest.fixture(scope="module")
def code_t5_config_path():
    """
    Path to CodeT5Processor config
    :return: Path
    """
    return Path(__file__).parent / "resources" / "codet5_processor.json"


@pytest.fixture(scope="module")
def code_t5_config(code_t5_config_path):
    """
    CodeT5Processor config by path
    :return: dict with CodeT5Processor configs
    """
    with open(code_t5_config_path, "r") as fr:
        config = json.load(fr)
        config["model_bin_path"] = Path(__file__).parent.parent / Path(config["model_bin_path"])
    return config
