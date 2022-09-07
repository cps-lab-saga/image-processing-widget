import cv2 as cv

from image_processing_widget.custom_components import SpinBoxSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import enum_border_types
from image_processing_widget.process_plugin import ProcessPlugin


class Gradients(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.operation = QtWidgets.QComboBox(self)
        self.operation.addItems(["Sobel", "Laplacian"])
        self.operation.currentTextChanged.connect(self.operations_changed)
        self.form_layout.addRow("Operation:", self.operation)

        self.ksize_control = QtWidgets.QComboBox(self)
        self.ksize_control.addItems(["1", "3", "5", "7"])
        self.form_layout.addRow("Kernel Size:", self.ksize_control)

        self.x_weight_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.x_weight_control.setSingleStep(0.01)
        self.x_weight_control.setRange(0, 1)
        self.form_layout.addRow("X Gradient Weighting:", self.x_weight_control)

        self.y_weight_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.y_weight_control.setSingleStep(0.01)
        self.y_weight_control.setRange(0, 1)
        self.form_layout.addRow("Y Gradient Weighting:", self.y_weight_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

        self.operations_changed(self.operation.currentText())

        self.operation.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.ksize_control.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.x_weight_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.y_weight_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.border_type.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        pass

    def operations_changed(self, text):
        if text == "Sobel":
            self.x_weight_control.setEnabled(True)
            self.y_weight_control.setEnabled(True)
        else:
            self.x_weight_control.setDisabled(True)
            self.y_weight_control.setDisabled(True)
        if text in ["Gaussian", "Bilateral Filtering"]:
            self.border_type.setEnabled(True)

    def process_img(self, img):
        operation = self.operation.currentText()
        ksize = int(self.ksize_control.currentText())
        x_weighting = self.x_weight_control.value()
        y_weighting = self.y_weight_control.value()
        border = enum_border_types[self.border_type.currentText()]

        if operation == "Sobel":
            grad_x = cv.Sobel(
                img, cv.CV_16S, 1, 0, ksize=ksize, scale=1, delta=0, borderType=border
            )
            grad_y = cv.Sobel(
                img, cv.CV_16S, 0, 1, ksize=ksize, scale=1, delta=0, borderType=border
            )
            return cv.addWeighted(
                cv.convertScaleAbs(grad_x),
                x_weighting,
                cv.convertScaleAbs(grad_y),
                y_weighting,
                0,
            )

        elif operation == "Laplacian":
            new_img = cv.Laplacian(img, cv.CV_16S, ksize=ksize)
            return cv.convertScaleAbs(new_img)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Gradients()
    widget.show()

    app.exec()
