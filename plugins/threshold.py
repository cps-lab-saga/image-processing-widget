import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import enum_thresholds
from image_processing_widget.plugin_objects import ProcessPlugin


class Thresholds(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.thresh_type = QtWidgets.QComboBox(self)
        self.thresh_type.addItems(enum_thresholds.keys())
        self.thresh_type.currentTextChanged.connect(self.operations_changed)
        self.form_layout.addRow("Type:", self.thresh_type)

        self.thresh_control = MySlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.thresh_control.setSingleStep(1)
        self.thresh_control.setRange(0, 2**8 - 1)
        self.form_layout.addRow("Threshold:", self.thresh_control)

    def connect_ui(self, update_func):
        self.thresh_type.currentTextChanged.connect(update_func)
        self.thresh_control.valueChanged.connect(update_func)

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        pass

    def process_img(self, img):
        thresh_type = enum_thresholds[self.thresh_type.currentText()]
        threshold = round(self.thresh_control.value())
        thresh, new_img = cv.threshold(img, threshold, 2**8 - 1, thresh_type)
        if thresh_type in [cv.THRESH_OTSU, cv.THRESH_TRIANGLE]:
            self.thresh_control.setValue(thresh)
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Thresholds()
    widget.show()

    app.exec()
