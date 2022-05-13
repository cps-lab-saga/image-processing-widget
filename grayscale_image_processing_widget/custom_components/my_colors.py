from grayscale_image_processing_widget.defs import QtGui

tab10_rgb = {
    "blue": (31, 119, 180),
    "orange": (255, 127, 14),
    "green": (44, 160, 44),
    "red": (214, 39, 40),
    "purple": (148, 103, 189),
    "brown": (140, 86, 75),
    "pink": (227, 119, 194),
    "gray": (127, 127, 127),
    "olive": (188, 189, 34),
    "cyan": (23, 190, 207),
}

tab10_qcolor = {k: QtGui.QColor(*v) for k, v in tab10_rgb.items()}
