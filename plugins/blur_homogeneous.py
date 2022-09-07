import cv2 as cv

from image_processing_widget.custom_components import SpinBoxSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class HomogenousBlur(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.x_control = SpinBoxSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.x_control.setSingleStep(1)
        self.x_control.setRange(1, 100)
        self.form_layout.addRow("Kernel Width:", self.x_control)

        self.y_control = SpinBoxSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.y_control.setSingleStep(1)
        self.y_control.setRange(1, 100)
        self.form_layout.addRow("Kernel Height:", self.y_control)

        self.x_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.y_control.valueChanged.connect(lambda _: self.settings_updated.emit())

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.x_control.setRange(1, lim)
        self.y_control.setRange(1, lim)

    def process_img(self, img):
        x = round(self.x_control.value())
        y = round(self.y_control.value())
        return cv.blur(img, (x, y))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HomogenousBlur()
    widget.show()

    app.exec()
