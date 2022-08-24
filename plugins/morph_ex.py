import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import (
    enum_morph_shapes,
    enum_border_types,
    enum_morph_types,
)
from image_processing_widget.plugin_objects import ProcessPlugin


class MorphEx(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.operation = QtWidgets.QComboBox(self)
        self.operation.addItems(enum_morph_types.keys())
        self.form_layout.addRow("Operation:", self.operation)

        self.shape = QtWidgets.QComboBox(self)
        self.shape.addItems(enum_morph_shapes.keys())
        self.form_layout.addRow("Shape:", self.shape)

        self.size_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.size_control.setSingleStep(1)
        self.size_control.setRange(0, 30)
        self.form_layout.addRow("Size:", self.size_control)

        self.iterations = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.iterations.setSingleStep(1)
        self.iterations.setRange(1, 100)
        self.form_layout.addRow("Iterations:", self.iterations)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.shape.currentTextChanged.connect(update_func)
        self.size_control.valueChanged.connect(update_func)
        self.border_type.currentTextChanged.connect(update_func)
        self.iterations.valueChanged.connect(update_func)
        self.operation.currentTextChanged.connect(update_func)

    def process_img(self, img):
        shape = enum_morph_shapes[self.shape.currentText()]
        size = round(self.size_control.value())
        border = enum_border_types[self.border_type.currentText()]
        operation = enum_morph_types[self.operation.currentText()]
        iterations = round(self.iterations.value())

        element = cv.getStructuringElement(
            shape, (2 * size + 1, 2 * size + 1), (-1, -1)
        )

        return cv.morphologyEx(
            img, operation, element, iterations=iterations, borderType=border
        )

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MorphEx()
    widget.show()

    app.exec()
