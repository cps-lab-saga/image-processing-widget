import cv2 as cv

from image_processing_widget.custom_components import SpinBoxRangeSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class Canny(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.threshold_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.threshold_range_control.setSingleStep(1)
        self.threshold_range_control.setRange(0, 2**8 - 1)
        self.threshold_range_control.setValue(0, 2**8 - 1)
        self.form_layout.addRow("Threshold:", self.threshold_range_control)

        self.ksize_control = QtWidgets.QComboBox(self)
        self.ksize_control.addItems(["3", "5", "7"])
        self.form_layout.addRow("Kernel Size:", self.ksize_control)

        self.grad_type = QtWidgets.QComboBox(self)
        self.grad_type.addItems(["|dI/dx|+|dI/dy|", "√((dI/dx)^2+(dI/dy)^2)"])
        self.form_layout.addRow("Gradient:", self.grad_type)

        self.grad_type.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.ksize_control.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.threshold_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        pass

    def process_img(self, img):
        if self.grad_type.currentText() == "|dI/dx|+|dI/dy|":
            l2grad = False
        elif self.grad_type.currentText() == "√((dI/dx)^2+(dI/dy)^2)":
            l2grad = True
        ksize = int(self.ksize_control.currentText())
        lower, upper = self.threshold_range_control.value()
        return cv.Canny(img, lower, upper, apertureSize=ksize, L2gradient=l2grad)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Canny()
    widget.show()

    app.exec()
