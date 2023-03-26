[![codecov](https://codecov.io/gh/gudarikon/image-to-code/branch/master/graph/badge.svg?token=JP2U7KJIGV)](https://codecov.io/gh/gudarikon/image-to-code)

# image-to-code
This repository contains code image dataset generator and NLP model for recognizing code from image
________
# CodeToImageGenerator
It works only on specific size monitor.

## Preparation

1. remove breadcrumbs:
  Click on the bottom panel showing current classes, methods, etc. (In this screenshot it shows RepoParser)
  
   ![img](https://user-images.githubusercontent.com/62846387/200181326-50657da7-1ae3-4245-8784-5b3647542ca8.png)

   Choose `Breadcrumbs` in the opened menu, pick `Don't Show`
   
   ![img_1](https://user-images.githubusercontent.com/62846387/200181331-f5979156-2284-440b-8554-41ee276a518b.png)



   *Later breadcrumbs are restored in
the* [Editor | General | Breadcrumbs](https://www.jetbrains.com/help/pycharm/settings-editor-breadcrumbs.html)
*menu.*

2. open terminal window:
   
   Click `Run` in the bottom panel
   
   ![img_2](https://user-images.githubusercontent.com/62846387/200181335-de2f7f34-d2dc-4e3d-ab60-786c697e9bb3.png)


   Move terminal window to the bottom.
   
   ![img_3](https://user-images.githubusercontent.com/62846387/200181338-fb38a055-634b-4735-b8c3-575a15e66919.png)

   
3. remove gutter icons: right click in gutter -> Configure Gutter Icons... -> Show gutter icons (Off)
4. open filetree and move it to the left, as far as it can go.
5. set language to English.
6. Compact View of inspections (top right corner)
7. Remove ligatures

## Config
config is stored in config.json. Here you can specify  data folders and change path to repository that is opened in intellij IDE. **If you manually moved Run panel or filetree panel, change visible_lines and visible_symbols to -1 and move it as you did in preparation steps**

## Stopping screenshots
If you want to stop the program, move your mouse during screenshots. The program will exit after current file is finished. All traversed files are saved.
________
# ImageToText

This part contains info about OCR processors used to extract text from the images.
Available solutions could be found in `src/image_to_text/processors/`

New solutions could be easily added using `src/image_to_text/processors/ocr_processor.py` base class. Don't forget to add custom processor to `src/image_to_text/processors.__init__` for convenient access via strings in `src/image_to_text/img_to_text.py `

## [Tesseract](https://github.com/tesseract-ocr/tesseract)

First of all one should install Tesseract on the machine.

> Install `Google Tesseract OCR <https://github.com/tesseract-ocr/tesseract>`_
  (additional info how to install the engine on Linux, Mac OSX and Windows).
  You must be able to invoke the tesseract command as *tesseract*. If this
  isn't the case, for example because tesseract isn't in your PATH, you will
  have to change the "tesseract_cmd" variable ``pytesseract.pytesseract.tesseract_cmd``.
  Under Debian/Ubuntu you can use the package **tesseract-ocr**.
  For Mac OS users. please install homebrew package **tesseract**.

Once Tesseract is installed the path to tessract.exe file should be added to the local `.env` file. See `.env.example` template
  
## [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

More advanced OCR for image processing. Supports text boxes which allow to add line spacing to the parsed text

## Config

All the processors classes contain `**kwargs` essential for the proper operation. Thus, `.json` formatted config templates are provided in `resources/configs/` 

________
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

________
# Deploy
Deploying via GitHub action .github/workflows/deploy_action.yml and run.sh

________
# Telegram Bot
[Image To Code Bot](https://t.me/image_to_code_bot)
is ready to receive images to return text and code from them
