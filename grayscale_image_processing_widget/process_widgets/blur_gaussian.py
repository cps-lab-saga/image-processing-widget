import cv2 as cv

from grayscale_image_processing_widget.custom_components.cv_enums import (
    enum_border_types,
)
from grayscale_image_processing_widget.custom_components.double_slider import (
    DoubleSlider,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class GaussianBlur(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.x_control = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.x_control.setSingleStep(1)
        self.x_control.setRange(1, 100)
        layout.addRow("Kernel Width:", self.x_control)

        self.y_control = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.y_control.setSingleStep(1)
        self.y_control.setRange(1, 100)
        layout.addRow("Kernel Height:", self.y_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.x_control.doubleValueChanged.connect(update_func)
        self.y_control.doubleValueChanged.connect(update_func)
        self.border_type.currentTextChanged.connect(update_func)

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.x_control.setRange(1, lim)
        self.y_control.setRange(1, lim)

    def process_img(self, img):
        border = enum_border_types[self.border_type.currentText()]
        x = round(self.x_control.value())
        y = round(self.y_control.value())
        if not x % 2:
            x += 1
        if not y % 2:
            y += 1
        new_img = cv.GaussianBlur(img, (x, y), border)
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = GaussianBlur()
    widget.show()

    app.exec()
