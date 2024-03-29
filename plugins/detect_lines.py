import math

import cv2 as cv
import numpy as np

from image_processing_widget.custom_components import SpinBoxRangeSlider, SpinBoxSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class DetectLines(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.operation = QtWidgets.QComboBox(self)
        self.operation.addItems(["Standard Hough Lines", "Probabilistic Hough Lines"])
        self.operation.currentTextChanged.connect(self.operations_changed)
        self.form_layout.addRow("Operation:", self.operation)

        self.rho_control = SpinBoxSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.rho_control.setSingleStep(0.01)
        self.rho_control.setRange(0.01, 1)
        self.rho_control.setValue(1)
        self.form_layout.addRow("Rho (Resolution):", self.rho_control)

        self.theta_control = SpinBoxSlider(decimals=2, orientation=QtCore.Qt.Horizontal)
        self.theta_control.setSingleStep(0.01)
        self.theta_control.setRange(0.01, 1)
        self.theta_control.setValue(1)
        self.form_layout.addRow("Theta (Resolution):", self.theta_control)

        self.threshold_control = SpinBoxSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.threshold_control.setSingleStep(1)
        self.threshold_control.setRange(0, 255)
        self.form_layout.addRow("Threshold:", self.threshold_control)

        self.theta_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.theta_range_control.setSingleStep(1)
        self.theta_range_control.setRange(0, 180)
        self.theta_range_control.setValue(0, 1)
        self.form_layout.addRow("Theta Range:", self.theta_range_control)

        self.min_length_control = SpinBoxSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.min_length_control.setSingleStep(1)
        self.min_length_control.setRange(0, 100)
        self.form_layout.addRow("Min Length:", self.min_length_control)

        self.max_gap_control = SpinBoxSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.max_gap_control.setSingleStep(1)
        self.max_gap_control.setRange(0, 255)
        self.form_layout.addRow("Max Gap:", self.max_gap_control)

        self.operations_changed(self.operation.currentText())

        self.rho_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.theta_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.threshold_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.theta_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.min_length_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.max_gap_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.operation.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def operations_changed(self, text):
        if text == "Standard Hough Lines":
            self.theta_range_control.setEnabled(True)
            self.min_length_control.setEnabled(False)
            self.max_gap_control.setEnabled(False)

        elif text == "Probabilistic Hough Lines":
            self.theta_range_control.setEnabled(False)
            self.min_length_control.setEnabled(True)
            self.max_gap_control.setEnabled(True)

    def process_img(self, img):
        if img.ndim > 2:
            raise Exception("Only available in grayscale mode.")

        rho = self.rho_control.value()
        theta = np.radians(self.theta_control.value())
        threshold = round(self.threshold_control.value())
        min_length = self.min_length_control.value()
        min_theta, max_theta = self.theta_range_control.value()
        max_gap = self.max_gap_control.value()
        operation = self.operation.currentText()
        if operation == "Standard Hough Lines":
            lines = cv.HoughLines(
                img, rho, theta, threshold, min_theta=min_theta, max_theta=max_theta
            )

            new_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            if lines is not None:
                for i in range(min([len(lines), 50])):
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = int(x0 + 1000 * -b), int(y0 + 1000 * a)
                    pt2 = int(x0 - 1000 * -b), int(y0 - 1000 * a)
                    cv.line(new_img, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
            return new_img
        elif operation == "Probabilistic Hough Lines":
            linesP = cv.HoughLinesP(
                img, rho, theta, threshold, minLineLength=min_length, maxLineGap=max_gap
            )

            new_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            if linesP is not None:
                for i in range(min([len(linesP), 50])):
                    l = linesP[i][0]
                    cv.line(
                        new_img, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA
                    )
            return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = DetectLines()
    widget.show()

    app.exec()
