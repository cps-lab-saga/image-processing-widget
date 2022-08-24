import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.funcs.cv_enums import (
    enum_morph_shapes,
    enum_border_types,
)
from image_processing_widget.plugin_objects import ProcessPlugin


class Erode(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.erosion_shape = QtWidgets.QComboBox(self)
        self.erosion_shape.addItems(enum_morph_shapes.keys())
        self.form_layout.addRow("Erosion Shape:", self.erosion_shape)

        self.erosion_size_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.erosion_size_control.setSingleStep(1)
        self.erosion_size_control.setRange(0, 30)
        self.form_layout.addRow("Erosion Size:", self.erosion_size_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.erosion_shape.currentTextChanged.connect(update_func)
        self.erosion_size_control.valueChanged.connect(update_func)
        self.border_type.currentTextChanged.connect(update_func)

    def process_img(self, img):
        erosion_shape = enum_morph_shapes[self.erosion_shape.currentText()]
        erosion_size = round(self.erosion_size_control.value())

        border = enum_border_types[self.border_type.currentText()]
        element = cv.getStructuringElement(
            erosion_shape,
            (2 * erosion_size + 1, 2 * erosion_size + 1),
            (erosion_size, erosion_size),
        )
        new_img = cv.erode(img, element, borderType=border)
        return new_img

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Erode()
    widget.show()

    app.exec()
