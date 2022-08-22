import cv2 as cv

from image_processing_widget.custom_components import ProcessBase, MySlider
from image_processing_widget.defs import QtCore, QtWidgets


class InRange(ProcessBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.lower_control = MySlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.lower_control.setSingleStep(1)
        self.lower_control.setRange(0, 2**8 - 1)
        self.lower_control.valueChanged.connect(self.keep_range)
        self.form_layout.addRow("Lower:", self.lower_control)

        self.upper_control = MySlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.upper_control.setSingleStep(1)
        self.upper_control.setRange(0, 2**8 - 1)
        self.upper_control.valueChanged.connect(self.keep_range)
        self.form_layout.addRow("Upper:", self.upper_control)

    def connect_ui(self, update_func):
        self.lower_control.valueChanged.connect(update_func)
        self.upper_control.valueChanged.connect(update_func)

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        pass

    def keep_range(self, val):
        if self.sender() == self.lower_control:
            if val > self.upper_control.value():
                self.blockSignals(True)
                self.upper_control.setValue(val)
                self.blockSignals(False)
        elif self.sender() == self.upper_control:
            if val < self.lower_control.value():
                self.blockSignals(True)
                self.lower_control.setValue(val)
                self.blockSignals(False)

    def process_img(self, img):
        lower = round(self.lower_control.value())
        upper = round(self.upper_control.value())
        return cv.inRange(img, lower, upper)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = InRange()
    widget.show()

    app.exec()
