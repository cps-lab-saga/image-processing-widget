import cv2 as cv
import numpy as np

from image_processing_widget.custom_components import SpinBoxRangeSlider, SpinBoxSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class DetectCircles(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.dp_control = SpinBoxSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.dp_control.setSingleStep(0.01)
        self.dp_control.setRange(1, 5)
        self.dp_control.setValue(1)
        self.form_layout.addRow("Resolution Ratio:", self.dp_control)

        self.min_dist_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.min_dist_control.setSingleStep(0.01)
        self.min_dist_control.setRange(1, 10)
        self.min_dist_control.setValue(1)
        self.form_layout.addRow("Min Distance:", self.min_dist_control)

        self.param1_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.param1_control.setSingleStep(1)
        self.param1_control.setRange(1, 255)
        self.param1_control.setValue(100)
        self.form_layout.addRow("Param1:", self.param1_control)

        self.param2_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.param2_control.setSingleStep(1)
        self.param2_control.setRange(1, 255)
        self.param2_control.setValue(100)
        self.form_layout.addRow("Param2:", self.param2_control)

        self.r_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.r_control.setSingleStep(1)
        self.r_control.setRange(0, 2**8 - 1)
        self.r_control.setValue(0, 2**8 - 1)
        self.form_layout.addRow("Radius:", self.r_control)

        self.dp_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.min_dist_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.param1_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.param2_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.r_control.valueChanged.connect(lambda _: self.settings_updated.emit())

    def adjust_range(self, shape):
        lim = min(shape[0], shape[1])
        self.min_dist_control.setRange(1, round(lim))
        self.r_control.setRange(0, round(lim))

    def process_img(self, img):
        if img.ndim > 2:
            raise Exception("Only accepts 8-bit binary source image")

        dp = self.dp_control.value()
        min_dist = self.min_dist_control.value()
        param1 = self.param1_control.value()
        param2 = self.param2_control.value()
        min_r, max_r = self.r_control.value()

        circles = cv.HoughCircles(
            img,
            cv.HOUGH_GRADIENT,
            dp,
            min_dist,
            param1=param1,
            param2=param2,
            minRadius=round(min_r),
            maxRadius=round(max_r),
        )

        new_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for count, i in enumerate(circles[0, :]):
                center = (i[0], i[1])
                # circle center
                cv.circle(new_img, center, 1, (255, 0, 0), 3)
                # circle outline
                radius = i[2]
                cv.circle(new_img, center, radius, (0, 0, 255), 3)
                if count > 20:
                    break
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = DetectCircles()
    widget.show()

    app.exec()
