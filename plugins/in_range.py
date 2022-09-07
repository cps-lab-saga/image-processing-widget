import cv2 as cv

from image_processing_widget.custom_components import SpinBoxRangeSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class InRange(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.range_control.setSingleStep(1)
        self.range_control.setRange(0, 2**8 - 1)
        self.range_control.setValue(0, 2**8 - 1)
        self.form_layout.addRow("Range:", self.range_control)

        self.range_control.valueChanged.connect(lambda _: self.settings_updated.emit())

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        pass

    def process_img(self, img):
        lower, upper = (round(x) for x in self.range_control.value())
        return cv.inRange(img, lower, upper)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = InRange()
    widget.show()

    app.exec()
