import cv2 as cv

from grayscale_image_processing_widget.custom_components.cv_enums import enum_thresholds
from grayscale_image_processing_widget.custom_components.double_slider import (
    DoubleSlider,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class Thresholds(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QFormLayout(self)

        self.thresh_type = QtWidgets.QComboBox(self)
        self.thresh_type.addItems(enum_thresholds.keys())
        self.thresh_type.currentTextChanged.connect(self.operations_changed)
        self.layout.addRow("Type:", self.thresh_type)

        self.thresh_control = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.thresh_control.setSingleStep(1)
        self.thresh_control.setRange(0, 2**8 - 1)
        self.layout.addRow("Threshold:", self.thresh_control)

    def connect_ui(self, update_func):
        self.thresh_type.currentTextChanged.connect(update_func)
        self.thresh_control.doubleValueChanged.connect(update_func)

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        pass

    def process_img(self, img):
        thresh_type = enum_thresholds[self.thresh_type.currentText()]
        threshold = round(self.thresh_control.value())

        thresh, new_img = cv.threshold(img, threshold, 2**8 - 1, thresh_type)
        if thresh_type == cv.THRESH_OTSU or thresh_type == cv.THRESH_TRIANGLE:
            self.thresh_control.setValue(thresh)
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Thresholds()
    widget.show()

    app.exec()
