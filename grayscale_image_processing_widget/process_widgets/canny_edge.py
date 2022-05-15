import cv2 as cv

from grayscale_image_processing_widget.custom_components.double_slider import (
    DoubleSlider,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class Canny(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QFormLayout(self)

        self.lower_thresh = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.lower_thresh.setSingleStep(1)
        self.lower_thresh.setRange(0, 2**8 - 1)
        self.lower_thresh.doubleValueChanged.connect(self.keep_range)
        self.layout.addRow("Lower:", self.lower_thresh)

        self.upper_thresh = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.upper_thresh.setSingleStep(1)
        self.upper_thresh.setRange(0, 2**8 - 1)
        self.upper_thresh.doubleValueChanged.connect(self.keep_range)
        self.layout.addRow("Upper:", self.upper_thresh)

        self.ksize_control = QtWidgets.QComboBox(self)
        self.ksize_control.addItems(["3", "5", "7"])
        self.layout.addRow("Kernel Size:", self.ksize_control)

        self.grad_type = QtWidgets.QComboBox(self)
        self.grad_type.addItems(["|dI/dx|+|dI/dy|", "√((dI/dx)^2+(dI/dy)^2)"])
        self.layout.addRow("Gradient:", self.grad_type)

    def connect_ui(self, update_func):
        self.grad_type.currentTextChanged.connect(update_func)
        self.ksize_control.currentTextChanged.connect(update_func)
        self.lower_thresh.doubleValueChanged.connect(update_func)
        self.upper_thresh.doubleValueChanged.connect(update_func)

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        pass

    def keep_range(self, val):
        if self.sender() == self.lower_thresh:
            if val > self.upper_thresh.value():
                self.blockSignals(True)
                self.upper_thresh.setValue(val)
                self.blockSignals(False)
        elif self.sender() == self.upper_thresh:
            if val < self.lower_thresh.value():
                self.blockSignals(True)
                self.lower_thresh.setValue(val)
                self.blockSignals(False)

    def process_img(self, img):
        if self.grad_type.currentText() == "|dI/dx|+|dI/dy|":
            l2grad = False
        elif self.grad_type.currentText() == "√((dI/dx)^2+(dI/dy)^2)":
            l2grad = True
        ksize = int(self.ksize_control.currentText())
        lower = round(self.lower_thresh.value())
        upper = round(self.upper_thresh.value())

        new_img = cv.Canny(img, lower, upper, apertureSize=ksize, L2gradient=l2grad)

        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Canny()
    widget.show()

    app.exec()