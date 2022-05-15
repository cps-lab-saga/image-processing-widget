import cv2 as cv
import numpy as np

from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtWidgets


class FitBoundary(QtWidgets.QWidget, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QFormLayout(self)

        self.boundary = QtWidgets.QComboBox(self)
        self.boundary.addItems(
            ["Convex Hull", "Min Bounding Box", "Min Bounding Circle", "Ellipse"]
        )
        self.layout.addRow("Find Boundary:", self.boundary)

    def connect_ui(self, update_func):
        self.boundary.currentTextChanged.connect(update_func)

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        img_binary = (img > 0).astype(np.uint8)
        points = cv.findNonZero(img_binary).squeeze()
        boundary = self.boundary.currentText()

        new_img = cv.cvtColor(img_binary * 255, cv.COLOR_GRAY2BGR)
        if boundary == "Convex Hull":
            hull = cv.convexHull(points)

            cv.drawContours(new_img, [hull], 0, (0, 0, 255), 2)
            return new_img

        elif boundary == "Min Bounding Box":
            rect = cv.minAreaRect(points)
            f_box = cv.boxPoints(rect)
            n_box = np.intp(f_box)

            cv.drawContours(new_img, [n_box], 0, (0, 0, 255), 2)
            return new_img

        elif boundary == "Min Bounding Circle":
            centre, radius = cv.minEnclosingCircle(points)

            cv.circle(
                new_img, tuple(round(x) for x in centre), round(radius), (0, 0, 255), 2
            )
            return new_img

        elif boundary == "Ellipse":
            rect = cv.fitEllipse(points)

            cv.ellipse(new_img, rect, (0, 0, 255), 2)
            return new_img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = FitBoundary()
    widget.show()

    app.exec()