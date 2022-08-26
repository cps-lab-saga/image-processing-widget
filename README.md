# An Image Processing Widget

GUI to explore OpenCV image processing functions.

## Installation

Download latest release from [here](https://github.com/fukuda-lab-saga/image-processing-widget/releases/latest/download/image-processing-widget.zip).

1. From packaged .exe file (Windows)
    - Download latest .exe file from releases.
    - Run .exe file
2. From wheel
    - Download latest wheel file from releases.
    - Install wheel `pip install <package-name>.whl`
    - Run widget `image_processing`

## Usage

The application will look for a config file [**image_processing_config.ini**] and a plugins folder [**plugins**] in its directory.

Drag and drop image onto widget.
![Screenshot 1](/screenshots/screenshot1.png?raw=true "Screenshot 1")

Select process and adjust parameters.
![Screenshot 2](/screenshots/screenshot2.png?raw=true "Screenshot 2")
![Screenshot 3](/screenshots/screenshot3.png?raw=true "Screenshot 3")

## Config

The plugins activated are listed after `process_plugins = `  and `roi_plugins = `  in the config file and are seperated by commas.
Add and remove these as needed. Available plugins can be found in the plugins folder and their names are shown in the .image-processing-plugin files.

There are 2 read modes (`grayscale` and `color`) and 2 display modes  (`auto` and `8-bit`). Change these as needed.
