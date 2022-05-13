import cv2 as cv

from grayscale_image_processing_widget.custom_components.double_slider import DoubleSlider
from grayscale_image_processing_widget.custom_components.gui_save_base import GuiSaveBase
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class InRange(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QFormLayout(self)

        self.lower_control = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.lower_control.setSingleStep(1)
        self.lower_control.setRange(0, 2**8 - 1)
        self.lower_control.doubleValueChanged.connect(self.keep_range)
        self.layout.addRow("Lower:", self.lower_control)

        self.upper_control = DoubleSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.upper_control.setSingleStep(1)
        self.upper_control.setRange(0, 2**8 - 1)
        self.upper_control.doubleValueChanged.connect(self.keep_range)
        self.layout.addRow("Upper:", self.upper_control)

    def connect_ui(self, update_func):
        self.lower_control.doubleValueChanged.connect(update_func)
        self.upper_control.doubleValueChanged.connect(update_func)

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

        new_img = cv.inRange(img, lower, upper)
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = InRange()
    widget.show()

    app.exec()
