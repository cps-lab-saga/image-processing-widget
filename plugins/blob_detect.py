import cv2 as cv

from image_processing_widget.custom_components import SpinBoxRangeSlider, SpinBoxSlider
from image_processing_widget.defs import QtCore, QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class BlobDetect(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.threshold_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.threshold_range_control.setSingleStep(1)
        self.threshold_range_control.setRange(0, 2**8 - 1)
        self.threshold_range_control.setValue(0, 2**8 - 1)
        self.form_layout.addRow("Threshold:", self.threshold_range_control)

        self.area_range_control = SpinBoxRangeSlider(
            decimals=0, orientation=QtCore.Qt.Horizontal
        )
        self.area_range_control.setSingleStep(1)
        self.area_range_control.setRange(1, 100)
        self.form_layout.addRow("Area:", self.area_range_control)

        self.circularity_range_control = SpinBoxRangeSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.circularity_range_control.setSingleStep(0.01)
        self.circularity_range_control.setRange(0.01, 1)
        self.form_layout.addRow("Circularity:", self.circularity_range_control)

        self.convexity_range_control = SpinBoxRangeSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.convexity_range_control.setSingleStep(0.01)
        self.convexity_range_control.setRange(0.01, 1)
        self.form_layout.addRow("Convexity:", self.convexity_range_control)

        self.inertia_range_control = SpinBoxRangeSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.inertia_range_control.setSingleStep(0.01)
        self.inertia_range_control.setRange(0.01, 1)
        self.form_layout.addRow("Inertia Ratio:", self.inertia_range_control)

        self.threshold_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.area_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.circularity_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.inertia_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        self.area_range_control.setRange(1, shape[0] * shape[1] / 4)

    def process_img(self, img):
        detector = self.setup_blob_detector()
        keypoints = detector.detect(img)

        if img.ndim == 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

        return cv.drawKeypoints(
            img,
            keypoints,
            None,
            color=(0, 0, 255),
            flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
        )

    def setup_blob_detector(self):
        min_thresh, max_thresh = self.threshold_range_control.value()
        min_area, max_area = self.area_range_control.value()
        min_circularity, max_circularity = self.circularity_range_control.value()
        min_convexity, max_convexity = self.convexity_range_control.value()
        min_inertia, max_inertia = self.inertia_range_control.value()

        params = cv.SimpleBlobDetector_Params()

        params.minThreshold = min_thresh
        params.maxThreshold = max_thresh

        params.filterByArea = True
        params.minArea = min_area
        params.maxArea = max_area

        params.filterByCircularity = True
        params.minCircularity = min_circularity
        params.maxCircularity = max_circularity

        params.filterByConvexity = True
        params.minConvexity = min_convexity
        params.maxConvexity = max_convexity

        params.filterByInertia = True
        params.minInertiaRatio = min_inertia
        params.maxInertiaRatio = max_inertia

        return cv.SimpleBlobDetector_create(params)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = BlobDetect()
    widget.show()

    app.exec()
