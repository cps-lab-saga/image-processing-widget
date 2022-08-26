import cv2 as cv

from image_processing_widget.defs import QtWidgets
from image_processing_widget.funcs.cv_enums import (
    enum_contour_retrieval_modes,
    enum_contour_approx_modes,
)
from image_processing_widget.process_plugin import ProcessPlugin


class FindContours(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.retrieval_mode = QtWidgets.QComboBox(self)
        self.retrieval_mode.addItems(enum_contour_retrieval_modes.keys())
        self.form_layout.addRow("Retrieval Mode:", self.retrieval_mode)

        self.approx_mode = QtWidgets.QComboBox(self)
        self.approx_mode.addItems(enum_contour_approx_modes.keys())
        self.form_layout.addRow("Approx Mode:", self.approx_mode)

        self.retrieval_mode.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.approx_mode.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        if img.ndim > 2:
            raise Exception("Only accepts 8-bit binary source image")

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
