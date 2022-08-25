import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import enum_border_types
from image_processing_widget.plugin_objects import ProcessPlugin


class BilateralFiltering(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.d_control = MySlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.d_control.setSingleStep(1)
        self.d_control.setRange(1, 100)
        self.form_layout.addRow("Diameter:", self.d_control)

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

        self.d_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.sigma_color_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.sigma_space_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.border_type.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.d_control.setRange(1, lim)

    def process_img(self, img):
        border = enum_border_types[self.border_type.currentText()]
        d = round(self.d_control.value())
        sigma_space = round(self.sigma_space_control.value())
        sigma_color = round(self.sigma_color_control.value())
        return cv.bilateralFilter(img, d, sigma_color, sigma_space, border)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = BilateralFiltering()
    widget.show()

    app.exec()
