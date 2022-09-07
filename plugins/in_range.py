import cv2 as cv
import numpy as np

from image_processing_widget.custom_components import SpinBoxRangeSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class InRange(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.operation = QtWidgets.QComboBox(self)
        self.operation.currentTextChanged.connect(self.operations_changed)
        self.form_layout.addRow("Representation:", self.operation)

        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.currentChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.main_layout.addLayout(self.stacked_layout)

        self.intensity_controls_widget = QtWidgets.QWidget(self)
        self.intensity_form_layout = QtWidgets.QFormLayout(
            self.intensity_controls_widget
        )
        self.intensity_form_layout.setContentsMargins(0, 0, 0, 0)
        self.operation.addItems(["Intensity"])
        self.stacked_layout.addWidget(self.intensity_controls_widget)

        self.intensity_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.intensity_range_control.setSingleStep(1)
        self.intensity_range_control.setRange(0, 2**8 - 1)
        self.intensity_range_control.setValue(0, 2**8 - 1)
        self.intensity_form_layout.addRow("Intensity:", self.intensity_range_control)

        self.rgb_controls_widget = QtWidgets.QWidget(self)
        self.rgb_form_layout = QtWidgets.QFormLayout(self.rgb_controls_widget)
        self.rgb_form_layout.setContentsMargins(0, 0, 0, 0)
        self.operation.addItems(["RGB"])
        self.stacked_layout.addWidget(self.rgb_controls_widget)

        self.red_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.red_range_control.setSingleStep(1)
        self.red_range_control.setRange(0, 2**8 - 1)
        self.red_range_control.setValue(0, 2**8 - 1)
        self.rgb_form_layout.addRow("Red:", self.red_range_control)

        self.green_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.green_range_control.setSingleStep(1)
        self.green_range_control.setRange(0, 2**8 - 1)
        self.green_range_control.setValue(0, 2**8 - 1)
        self.rgb_form_layout.addRow("Green:", self.green_range_control)

        self.blue_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.blue_range_control.setSingleStep(1)
        self.blue_range_control.setRange(0, 2**8 - 1)
        self.blue_range_control.setValue(0, 2**8 - 1)
        self.rgb_form_layout.addRow("Blue:", self.blue_range_control)

        self.hsv_controls_widget = QtWidgets.QWidget(self)
        self.hsv_form_layout = QtWidgets.QFormLayout(self.hsv_controls_widget)
        self.hsv_form_layout.setContentsMargins(0, 0, 0, 0)
        self.operation.addItems(["HSV"])
        self.stacked_layout.addWidget(self.hsv_controls_widget)

        self.hue_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.hue_range_control.setSingleStep(1)
        self.hue_range_control.setRange(0, 2**8 - 1)
        self.hue_range_control.setValue(0, 2**8 - 1)
        self.hsv_form_layout.addRow("Hue:", self.hue_range_control)

        self.sat_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.sat_range_control.setSingleStep(1)
        self.sat_range_control.setRange(0, 2**8 - 1)
        self.sat_range_control.setValue(0, 2**8 - 1)
        self.hsv_form_layout.addRow("Sat:", self.sat_range_control)

        self.val_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.val_range_control.setSingleStep(1)
        self.val_range_control.setRange(0, 2**8 - 1)
        self.val_range_control.setValue(0, 2**8 - 1)
        self.hsv_form_layout.addRow("Val:", self.val_range_control)

        self.intensity_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.red_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.green_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.blue_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.hue_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.sat_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.val_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        self.stacked_layout.setCurrentIndex(self.operation.currentIndex())

    def process_img(self, img):
        operation = self.operation.currentText()

        if operation == "Intensity":
            lower, upper = (round(x) for x in self.intensity_range_control.value())
            return cv.inRange(img, lower, upper)
        elif operation == "RGB":
            r_lower, r_upper = (round(x) for x in self.red_range_control.value())
            g_lower, g_upper = (round(x) for x in self.green_range_control.value())
            b_lower, b_upper = (round(x) for x in self.blue_range_control.value())
            if img.ndim == 2:
                img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            return cv.inRange(
                img,
                np.array([r_lower, g_lower, b_lower]),
                np.array([r_upper, g_upper, b_upper]),
            )
        elif operation == "HSV":
            h_lower, h_upper = (round(x) for x in self.hue_range_control.value())
            s_lower, s_upper = (round(x) for x in self.sat_range_control.value())
            v_lower, v_upper = (round(x) for x in self.val_range_control.value())
            if img.ndim == 2:
                img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            return cv.inRange(
                hsv,
                np.array([h_lower, s_lower, v_lower]),
                np.array([h_upper, s_upper, v_upper]),
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = InRange()
    widget.show()

    app.exec()
