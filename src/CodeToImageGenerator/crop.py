import json

from PIL import Image

from CodeToImageGenerator.config import create_config


def crop_code(json_file_path, json_file_id, json_cropped_folder_path="C:/data/cropped_code"):
    with open(json_file_path, "r") as file:
        json_file = json.loads(file.read())
        json_file['code'] = json_file['code'][:len(json_file['code']) - 1]
    print(json_cropped_folder_path + str(json_file_id) + ".json")
    with open(json_cropped_folder_path + "/" + str(json_file_id) + ".json", "w") as write_file:
        write_file.write(json.dumps(json_file))


def crop_image(image_file_path, json_file_id,
               json_cropped_folder_path="C:/data/cropped_code_images"):
    image_file = Image.open(image_file_path)
    width, height = image_file.size
    image_file = image_file.crop(box=(0, 0, width, height - 27))
    image_file.save(json_cropped_folder_path + "/" + str(json_file_id) + ".png")


if __name__ == "__main__":
    config = create_config()
    for i in range(1, config.id):
        crop_code(config.code_folder + "/" + str(i) + ".json", i)
        crop_image(config.screenshot_code_folder + "/" + str(i) + ".png", i)
