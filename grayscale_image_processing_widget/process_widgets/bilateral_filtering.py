import cv2 as cv

from grayscale_image_processing_widget.custom_components.cv_enums import enum_border_types
from grayscale_image_processing_widget.custom_components.double_slider import DoubleSlider
from grayscale_image_processing_widget.custom_components.gui_save_base import GuiSaveBase
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class BilateralFiltering(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.d_control = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.d_control.setSingleStep(1)
        self.d_control.setRange(1, 100)
        layout.addRow("Diameter:", self.d_control)

        self.sigma_color_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.sigma_color_control.setSingleStep(1)
        self.sigma_color_control.setRange(1, 100)
        layout.addRow("Sigma Color:", self.sigma_color_control)

        self.sigma_space_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.sigma_space_control.setSingleStep(1)
        self.sigma_space_control.setRange(1, 100)
        layout.addRow("Sigma Space:", self.sigma_space_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.d_control.doubleValueChanged.connect(update_func)
        self.sigma_color_control.doubleValueChanged.connect(update_func)
        self.sigma_space_control.doubleValueChanged.connect(update_func)
        self.border_type.currentTextChanged.connect(update_func)

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.d_control.setRange(1, lim)

    def process_img(self, img):
        border = enum_border_types[self.border_type.currentText()]
        d = round(self.d_control.value())
        sigma_space = round(self.sigma_space_control.value())
        sigma_color = round(self.sigma_color_control.value())
        new_img = cv.bilateralFilter(img, d, sigma_color, sigma_space, border)
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = BilateralFiltering()
    widget.show()

    app.exec()
