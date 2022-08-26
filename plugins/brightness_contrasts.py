import cv2 as cv

from image_processing_widget.custom_components import MySlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class BrightnessContrasts(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.brightness_control = MySlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.brightness_control.setSingleStep(1)
        self.brightness_control.setRange(0, 100)
        self.form_layout.addRow("Brightness:", self.brightness_control)

        self.contrast_control = MySlider(
            decimals=2, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.contrast_control.setSingleStep(0.01)
        self.contrast_control.setRange(1, 3)
        self.form_layout.addRow("Contrasts:", self.contrast_control)

        self.brightness_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.contrast_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def process_img(self, img):
        alpha = self.contrast_control.value()
        beta = self.brightness_control.value()
        return cv.convertScaleAbs(img, alpha=alpha, beta=beta)

    def adjust_range(self, shape):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = BrightnessContrasts()
    widget.show()

    app.exec()
