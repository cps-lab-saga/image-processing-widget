import cv2 as cv

from image_processing_widget.defs import QtWidgets
from image_processing_widget.funcs.cv_enums import enum_aruco_dict
from image_processing_widget.process_plugin import ProcessPlugin
from .funcs import aruco_display


class ArucoDetect(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.aruco_set = QtWidgets.QComboBox(self)
        self.aruco_set.addItems(enum_aruco_dict.keys())
        self.form_layout.addRow("Aruco Set:", self.aruco_set)

        self.aruco_set.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def process_img(self, img):
        aruco_dict = cv.aruco.getPredefinedDictionary(
            enum_aruco_dict[self.aruco_set.currentText()]
        )
        aruco_params = cv.aruco.DetectorParameters()
        aruco_detector = cv.aruco.ArucoDetector(aruco_dict, aruco_params)

        corners, ids, rejected = aruco_detector.detectMarkers(img)

        if len(corners) > 0 and img.ndim <= 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            return aruco_display(corners, ids, img)
        else:
            return img
