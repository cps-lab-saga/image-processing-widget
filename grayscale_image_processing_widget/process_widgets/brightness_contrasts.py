import cv2 as cv

from grayscale_image_processing_widget.custom_components.double_slider import DoubleSlider
from grayscale_image_processing_widget.custom_components.gui_save_base import GuiSaveBase
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class BrightnessContrasts(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.brightness_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.brightness_control.setSingleStep(1)
        self.brightness_control.setRange(0, 100)
        layout.addRow("Brightness:", self.brightness_control)

        self.contrast_control = DoubleSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.contrast_control.setSingleStep(0.01)
        self.contrast_control.setRange(1, 3)
        layout.addRow("Contrasts:", self.contrast_control)

    def connect_ui(self, update_func):
        self.brightness_control.doubleValueChanged.connect(update_func)
        self.contrast_control.doubleValueChanged.connect(update_func)

    def process_img(self, img):
        alpha = self.contrast_control.value()
        beta = self.brightness_control.value()
        new_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
        return new_img

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = BrightnessContrasts()
    widget.show()

    app.exec()
