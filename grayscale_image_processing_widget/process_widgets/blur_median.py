import cv2 as cv

from grayscale_image_processing_widget.custom_components.double_slider import DoubleSlider
from grayscale_image_processing_widget.custom_components.gui_save_base import GuiSaveBase
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class MedianBlur(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QtWidgets.QFormLayout(self)

        self.ksize_control = DoubleSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal, parent=self
        )
        self.ksize_control.setSingleStep(1)
        self.ksize_control.setRange(1, 100)
        layout.addRow("Kernel Size:", self.ksize_control)

    def connect_ui(self, update_func):
        self.ksize_control.doubleValueChanged.connect(update_func)

    def adjust_range(self, shape):
        lim = round((shape[0] + shape[1]) / 2 * 0.1)
        self.ksize_control.setRange(1, lim)

    def process_img(self, img):
        ksize = round(self.ksize_control.value())
        if not ksize % 2:
            ksize += 1
        new_img = cv.medianBlur(img, ksize)
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MedianBlur()
    widget.show()

    app.exec()
