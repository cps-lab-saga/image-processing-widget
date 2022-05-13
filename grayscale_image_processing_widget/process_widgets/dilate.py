import cv2 as cv

from grayscale_image_processing_widget.custom_components.cv_enums import enum_morph_shapes, enum_border_types
from grayscale_image_processing_widget.custom_components.double_slider import DoubleSlider
from grayscale_image_processing_widget.custom_components.gui_save_base import GuiSaveBase
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class Dilate(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.dilation_shape = QtWidgets.QComboBox(self)
        self.dilation_shape.addItems(enum_morph_shapes.keys())
        layout.addRow("Dilation Shape:", self.dilation_shape)

        self.dilatation_size_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.dilatation_size_control.setSingleStep(1)
        self.dilatation_size_control.setRange(0, 30)
        layout.addRow("Dilation Size:", self.dilatation_size_control)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        layout.addRow("Border Types:", self.border_type)

    def connect_ui(self, update_func):
        self.dilation_shape.currentTextChanged.connect(update_func)
        self.dilatation_size_control.doubleValueChanged.connect(update_func)
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
        new_img = cv.dilate(img, element, borderType=border)
        return new_img

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Dilate()
    widget.show()

    app.exec()
