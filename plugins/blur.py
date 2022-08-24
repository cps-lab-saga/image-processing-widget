import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import enum_border_types
from image_processing_widget.plugin_objects import ProcessPlugin


class Blur(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.operation = QtWidgets.QComboBox(self)
        self.operation.addItems(
            ["Homogeneous", "Gaussian", "Median", "Bilateral Filtering"]
        )
        self.operation.currentTextChanged.connect(self.operations_changed)
        self.form_layout.addRow("Operation:", self.operation)

        self.x_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.x_control.setSingleStep(1)
        self.x_control.setRange(1, 100)
        self.x_control.valueChanged.connect(self.make_square)
        self.form_layout.addRow("Kernel Width:", self.x_control)

        self.y_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.y_control.setSingleStep(1)
        self.y_control.setRange(1, 100)
        self.y_control.valueChanged.connect(self.make_square)
        self.form_layout.addRow("Kernel Height:", self.y_control)

        self.sigma_color_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.sigma_color_control.setSingleStep(1)
        self.sigma_color_control.setRange(1, 100)
        self.form_layout.addRow("Sigma Color:", self.sigma_color_control)

        self.sigma_space_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.sigma_space_control.setSingleStep(1)
        self.sigma_space_control.setRange(1, 100)
        self.form_layout.addRow("Sigma Space:", self.sigma_space_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

        self.operations_changed(self.operation.currentText())

    def connect_ui(self, update_func):
        self.x_control.valueChanged.connect(update_func)
        self.y_control.valueChanged.connect(update_func)
        self.sigma_color_control.valueChanged.connect(update_func)
        self.sigma_space_control.valueChanged.connect(update_func)
        self.border_type.currentTextChanged.connect(update_func)
        self.operation.currentTextChanged.connect(update_func)

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.x_control.setRange(1, lim)
        self.y_control.setRange(1, lim)

    def operations_changed(self, text):
        if text == "Bilateral Filtering":
            self.sigma_space_control.setEnabled(True)
            self.sigma_color_control.setEnabled(True)
        else:
            self.sigma_space_control.setDisabled(True)
            self.sigma_color_control.setDisabled(True)
        if text in ["Gaussian", "Bilateral Filtering"]:
            self.border_type.setEnabled(True)
        else:
            self.border_type.setDisabled(True)
        self.make_square(self.x_control.value())

    def make_square(self, val):
        if self.operation.currentText() in ["Median", "Bilateral Filtering"]:
            self.blockSignals(True)
            self.x_control.setValue(val)
            self.y_control.setValue(val)
            self.blockSignals(False)

    def process_img(self, img):
        x = round(self.x_control.value())
        y = round(self.y_control.value())
        border = enum_border_types[self.border_type.currentText()]
        sigma_space = round(self.sigma_space_control.value())
        sigma_color = round(self.sigma_color_control.value())
        operation = self.operation.currentText()

        if operation == "Homogeneous":
            return cv.blur(img, (x, y))

        elif operation == "Gaussian":
            if not x % 2:  # make odd
                x += 1
            if not y % 2:
                y += 1
            return cv.GaussianBlur(img, (x, y), border)

        elif operation == "Median":
            if not x % 2:  # make odd
                x += 1
            return cv.medianBlur(img, x)

        elif operation == "Bilateral Filtering":
            return cv.bilateralFilter(img, x, sigma_color, sigma_space, border)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Blur()
    widget.show()

    app.exec()
