[![codecov](https://codecov.io/gh/gudarikon/image-to-code/branch/master/graph/badge.svg?token=JP2U7KJIGV)](https://codecov.io/gh/gudarikon/image-to-code)

# image-to-code

This repository contains code image dataset generator and NLP model for recognizing code from image

# Code to image dataset generator

Dataset generator is separate tool from the whole pipeline. It was created specifically for this
project to generate dataset which contains code and its screenshots.

Generated datasets:

1. [Code blocks screenshots](https://www.kaggle.com/datasets/alexeykononov5041/java-code-screenshots)
2. [Functions screenshots](https://www.kaggle.com/datasets/alexeykononov5041/java-code-search-net-function-screenshots)

## Requirements

1. an IntelliJ IDE for any language:
    * IntelliJ IDEA
    * PyCharm
    * GoLand
    * PhpStorm
    * etc
2. 1920x1080 resolution screen

## How to use

Image generator works in two modes: code blocks screenshots and functions screenshots.

### Preparation

1. remove breadcrumbs:
   Right lick on the bottom panel showing current classes, methods, etc. (In this screenshot it
   shows `OCRProcessor>process_image()`)

   ![breadcrumbs.png](resources/images/breadcrumbs.png)

   Choose `Breadcrumbs` in the opened menu, pick `Don't Show`

   *Later breadcrumbs are restored in
   the* [Editor | General | Breadcrumbs](https://www.jetbrains.com/help/pycharm/settings-editor-breadcrumbs.html)
   *menu.*

2. open terminal window:

   Click `Run` in the bottom panel. Move opened window to the bottom.

   ![run.png](resources/images/run.png)

3. remove gutter icons: right click in gutter | Configure Gutter Icons... | Show gutter icons
4. open filetree and move it to the maximal left position.
5. set language to English.
6. Compact View of inspections (top right corner)

   ![inspections.png](resources/images/inspections.png)

7. Remove ligatures
   in [Editor | Font | Enable ligatures](https://www.jetbrains.com/webstorm/guide/tips/font-ligatures/)

### Using code blocks screenshots

1. open IntelliJ project
2. set `repo_path` in config.json to project path
3. run `code_to_image/main_code_blocks.py`

### Using functions screenshots

1. create empty IntelliJ project
2. run `dataset_parser.py`, with `repo_path` in config.json set to empty
   project, `code_search_functions_path` to jsonl dataset
   from [code search net](https://huggingface.co/datasets/code_search_net)
3. run `code_to_image/main_functions.py`

### Config

Config is stored in config.json. Here you can specify data folders and change path to repository
that is opened in intellij IDE. **If you manually moved Run panel or filetree panel, change
visible_lines and visible_symbols to -1 and move it as you did in preparation steps**

### Stopping screenshots

If you want to stop the program, move your mouse during screenshots. The program will exit after
current file is finished. All traversed files are saved.

# ~~Tesseract~~

TODO: Fill info about used OCR

First of all one should install Tesseract on its his/her device.

- Install `Google Tesseract OCR <https://github.com/tesseract-ocr/tesseract>`_
  (additional info how to install the engine on Linux, Mac OSX and Windows).
  You must be able to invoke the tesseract command as *tesseract*. If this
  isn't the case, for example because tesseract isn't in your PATH, you will
  have to change the "tesseract_cmd" variable ``pytesseract.pytesseract.tesseract_cmd``.
  Under Debian/Ubuntu you can use the package **tesseract-ocr**.
  For Mac OS users. please install homebrew package **tesseract**.

You may use function from scr/ImageToTextGenerator via click command to check functionality

# Text2Code

UPD: we settled on [T5Code](https://github.com/salesforce/CodeT5)

# Inference

For launching the whole pipeline you can do the following:

```shell
cd image-to-code
```

```shell
/image-to-code$ PYTHONPATH=./ python3 \
                src/telegram_handler/pipeline_manager.py \
                /path/to/image.png
```

# Deploy

Deploying via GitHub action .github/workflows/deploy_action.yml and run.sh
