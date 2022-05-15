import cv2 as cv

from grayscale_image_processing_widget.custom_components.double_slider import (
    DoubleSlider,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class HomogenousBlur(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.x_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.x_control.setSingleStep(1)
        self.x_control.setRange(1, 100)
        layout.addRow("Kernel Width:", self.x_control)

        self.y_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.y_control.setSingleStep(1)
        self.y_control.setRange(1, 100)
        layout.addRow("Kernel Height:", self.y_control)

    def connect_ui(self, update_func):
        self.x_control.doubleValueChanged.connect(update_func)
        self.y_control.doubleValueChanged.connect(update_func)

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.x_control.setRange(1, lim)
        self.y_control.setRange(1, lim)

    def process_img(self, img):
        x = round(self.x_control.value())
        y = round(self.y_control.value())
        new_img = cv.blur(img, (x, y))
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HomogenousBlur()
    widget.show()

    app.exec()