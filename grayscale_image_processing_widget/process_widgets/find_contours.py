import cv2 as cv

from grayscale_image_processing_widget.custom_components.cv_enums import (
    enum_contour_retrieval_modes,
    enum_contour_approx_modes,
)
from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtWidgets


class FindContours(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QFormLayout(self)

        self.retrieval_mode = QtWidgets.QComboBox(self)
        self.retrieval_mode.addItems(enum_contour_retrieval_modes.keys())
        self.layout.addRow("Retrieval Mode:", self.retrieval_mode)

        self.approx_mode = QtWidgets.QComboBox(self)
        self.approx_mode.addItems(enum_contour_approx_modes.keys())
        self.layout.addRow("Approx Mode:", self.approx_mode)

    def connect_ui(self, update_func):
        self.retrieval_mode.currentTextChanged.connect(update_func)
        self.approx_mode.currentTextChanged.connect(update_func)

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        retrieval_mode = enum_contour_retrieval_modes[self.retrieval_mode.currentText()]

        approx_mode = enum_contour_approx_modes[self.approx_mode.currentText()]

        contours, hierarchy = cv.findContours(img, retrieval_mode, approx_mode)

        new_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        for i in range(len(contours)):
            cv.drawContours(
                new_img, contours, i, (0, 0, 255), 2, cv.LINE_8, hierarchy, 0
            )
        return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = FindContours()
    widget.show()

    app.exec()
