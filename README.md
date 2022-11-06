# image-to-code
This repository contains code image dataset generator and NLP model for recognizing code from image

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

## Config
config is stored in config.json. Here you can specify  data folders and change path to repository that is opened in intellij IDE. **If you manually moved Run panel or filetree panel, change visible_lines and visible_symbols to -1 and move it as you did in preparation steps**

## Stopping screenshots
If you want to stop the program, move your mouse during screenshots. The program will exit after current file is finished. All traversed files are saved.

# Tesseract
