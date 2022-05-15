import cv2 as cv

from grayscale_image_processing_widget.custom_components.cv_enums import (
    enum_morph_shapes,
    enum_border_types,
    enum_morph_types,
)
from grayscale_image_processing_widget.custom_components.double_slider import (
    DoubleSlider,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class MorphEx(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.operation = QtWidgets.QComboBox(self)
        self.operation.addItems(enum_morph_types.keys())
        layout.addRow("Operation:", self.operation)

        self.shape = QtWidgets.QComboBox(self)
        self.shape.addItems(enum_morph_shapes.keys())
        layout.addRow("Shape:", self.shape)

        self.size_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.size_control.setSingleStep(1)
        self.size_control.setRange(0, 30)
        layout.addRow("Size:", self.size_control)

        self.iterations = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.iterations.setSingleStep(1)
        self.iterations.setRange(1, 100)
        layout.addRow("Iterations:", self.iterations)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.shape.currentTextChanged.connect(update_func)
        self.size_control.doubleValueChanged.connect(update_func)
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
            shape, (2 * size + 1, 2 * size + 1), (size, size)
        )

        new_img = cv.morphologyEx(
            img, operation, element, iterations=iterations, borderType=border
        )

        return new_img

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MorphEx()
    widget.show()

    app.exec()
