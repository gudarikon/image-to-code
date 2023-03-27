import json
from math import floor

from PIL import Image

from src.code_to_image.main_code_blocks import LINE_HEIGHT
from .config_builder import ConfigBuilder


def crop_code(json_file_path: str, json_file_id: int,
              json_cropped_folder_path: str):
    with open(json_file_path, "r") as file:
        json_file = json.loads(file.read())
        json_file['code'] = json_file['code'][:len(json_file['code']) - 1]
    with open(json_cropped_folder_path + "/" + str(json_file_id) + ".json", "w") as write_file:
        write_file.write(json.dumps(json_file))


def crop_image(image_file_path: str, json_file_id: int,
               json_cropped_folder_path: str):
    image_file = Image.open(image_file_path)
    width, height = image_file.size
    image_file = image_file.crop(box=(0, 0, width, height - floor(LINE_HEIGHT)))
    image_file.save(json_cropped_folder_path + "/" + str(json_file_id) + ".png")


if __name__ == "__main__":
    config = ConfigBuilder().get_config()
    for i in range(1, config.id):
        crop_code(config.code_folder + "/" + str(i) + ".json", i,
                  config.code_folder + "/" + str(i) + ".json")
        crop_image(config.screenshot_code_folder + "/" + str(i) + ".png", i,
                   config.screenshot_code_folder + "/" + str(i) + ".png")
