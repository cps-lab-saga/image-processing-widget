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

        self.area_control = SpinBoxSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.area_control.setSingleStep(1)
        self.area_control.setRange(0, 100)
        self.form_layout.addRow("Area:", self.area_control)

        self.circularity_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.circularity_control.setSingleStep(0.01)
        self.circularity_control.setRange(0, 1)
        self.form_layout.addRow("Circularity:", self.circularity_control)

        self.convexity_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.convexity_control.setSingleStep(0.01)
        self.convexity_control.setRange(0, 1)
        self.form_layout.addRow("Convexity:", self.convexity_control)

        self.inertia_control = SpinBoxSlider(
            decimals=2, orientation=QtCore.Qt.Horizontal
        )
        self.inertia_control.setSingleStep(0.01)
        self.inertia_control.setRange(0, 1)
        self.form_layout.addRow("Inertia:", self.inertia_control)

        self.threshold_range_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.area_control.valueChanged.connect(lambda _: self.settings_updated.emit())
        self.circularity_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.inertia_control.valueChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def adjust_range(self, shape):
        self.area_control.setRange(0, shape[0] * shape[1] / 4)

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
        area = self.area_control.value()
        circularity = self.circularity_control.value()
        convexity = self.convexity_control.value()
        inertia = self.inertia_control.value()

        params = cv.SimpleBlobDetector_Params()

        params.minThreshold = min_thresh
        params.maxThreshold = max_thresh

        params.filterByArea = True
        params.minArea = area

        params.filterByCircularity = True
        params.minCircularity = circularity

        params.filterByConvexity = True
        params.minConvexity = convexity

        params.filterByInertia = True
        params.minInertiaRatio = inertia

        return cv.SimpleBlobDetector_create(params)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = BlobDetect()
    widget.show()

    app.exec()
