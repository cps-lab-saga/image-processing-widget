import cv2 as cv
import numpy as np

from grayscale_image_processing_widget.custom_components.double_slider import (
    DoubleSlider,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class DetectCircles(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QFormLayout(self)

        self.dp_control = DoubleSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.dp_control.setSingleStep(0.01)
        self.dp_control.setRange(1, 5)
        self.dp_control.setValue(1)
        self.layout.addRow("Resolution Ratio:", self.dp_control)

        self.min_dist_control = DoubleSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.min_dist_control.setSingleStep(0.01)
        self.min_dist_control.setRange(1, 10)
        self.min_dist_control.setValue(1)
        self.layout.addRow("Min Distance:", self.min_dist_control)

        self.param1_control = DoubleSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.param1_control.setSingleStep(1)
        self.param1_control.setRange(1, 255)
        self.param1_control.setValue(100)
        self.layout.addRow("Param1:", self.param1_control)

        self.param2_control = DoubleSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.param2_control.setSingleStep(1)
        self.param2_control.setRange(1, 255)
        self.param2_control.setValue(100)
        self.layout.addRow("Param2:", self.param2_control)

        self.min_r_control = DoubleSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.min_r_control.setSingleStep(1)
        self.min_r_control.setRange(0, 255)
        self.min_r_control.setValue(100)
        self.layout.addRow("Minimum Radius:", self.min_r_control)

        self.max_r_control = DoubleSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.max_r_control.setSingleStep(1)
        self.max_r_control.setRange(0, 255)
        self.max_r_control.setValue(100)
        self.layout.addRow("Maximum Radius:", self.max_r_control)

    def connect_ui(self, update_func):
        self.dp_control.doubleValueChanged.connect(update_func)
        self.min_dist_control.doubleValueChanged.connect(update_func)
        self.param1_control.doubleValueChanged.connect(update_func)
        self.param2_control.doubleValueChanged.connect(update_func)
        self.min_r_control.doubleValueChanged.connect(update_func)
        self.max_r_control.doubleValueChanged.connect(update_func)

    def adjust_range(self, shape):
        lim = (shape[0] + shape[1]) / 2
        self.min_dist_control.setRange(1, round(lim * 0.5))
        self.min_r_control.setRange(0, round(lim * 0.8))
        self.max_r_control.setRange(0, round(lim * 0.8))

    def process_img(self, img):
        dp = self.dp_control.value()
        min_dist = self.min_dist_control.value()
        param1 = self.param1_control.value()
        param2 = self.param2_control.value()
        min_r = round(self.min_r_control.value())
        max_r = round(self.max_r_control.value())

        circles = cv.HoughCircles(
            img,
            cv.HOUGH_GRADIENT,
            dp,
            min_dist,
            param1=param1,
            param2=param2,
            minRadius=min_r,
            maxRadius=max_r,
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