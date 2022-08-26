import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import enum_border_types
from image_processing_widget.process_plugin import ProcessPlugin


class GaussianBlur(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.x_control = MySlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.x_control.setSingleStep(1)
        self.x_control.setRange(1, 100)
        self.form_layout.addRow("Kernel Width:", self.x_control)

        self.y_control = MySlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.y_control.setSingleStep(1)
        self.y_control.setRange(1, 100)
        self.form_layout.addRow("Kernel Height:", self.y_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

        self.x_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.y_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.border_type.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

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
        return cv.GaussianBlur(img, (x, y), border)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = GaussianBlur()
    widget.show()

    app.exec()
