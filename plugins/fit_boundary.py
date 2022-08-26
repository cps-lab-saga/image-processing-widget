import cv2 as cv
import numpy as np

from image_processing_widget.defs import QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class FitBoundary(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.boundary = QtWidgets.QComboBox(self)
        self.boundary.addItems(
            ["Convex Hull", "Min Bounding Box", "Min Bounding Circle", "Ellipse"]
        )
        self.form_layout.addRow("Find Boundary:", self.boundary)

        self.boundary.currentTextChanged.connect(lambda _: self.settings_updated.emit())

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        if img.ndim > 2:
            raise Exception("Only accepts 8-bit binary source image")

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
