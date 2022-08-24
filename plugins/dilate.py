import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import (
    enum_morph_shapes,
    enum_border_types,
)
from image_processing_widget.plugin_objects import ProcessPlugin


class Dilate(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.dilation_shape = QtWidgets.QComboBox(self)
        self.dilation_shape.addItems(enum_morph_shapes.keys())
        self.form_layout.addRow("Dilation Shape:", self.dilation_shape)

        self.dilatation_size_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.dilatation_size_control.setSingleStep(1)
        self.dilatation_size_control.setRange(0, 30)
        self.form_layout.addRow("Dilation Size:", self.dilatation_size_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.dilation_shape.currentTextChanged.connect(update_func)
        self.dilatation_size_control.valueChanged.connect(update_func)
        self.border_type.currentTextChanged.connect(update_func)

    def process_img(self, img):
        dilation_shape = enum_morph_shapes[self.dilation_shape.currentText()]
        dilation_size = round(self.dilatation_size_control.value())
        border = enum_border_types[self.border_type.currentText()]
        element = cv.getStructuringElement(
            dilation_shape,
            (2 * dilation_size + 1, 2 * dilation_size + 1),
            (dilation_size, dilation_size),
        )

        return cv.dilate(img, element, borderType=border)

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Dilate()
    widget.show()

    app.exec()
