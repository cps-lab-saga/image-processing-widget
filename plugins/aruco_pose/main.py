from pathlib import Path

import cv2 as cv
import qtawesome as qta

from image_processing_widget.custom_components import PathEdit
from image_processing_widget.defs import QtWidgets, QtCore
from image_processing_widget.funcs import enum_aruco_dict, load_intrinsic
from image_processing_widget.process_plugin import ProcessPlugin
from .funcs import aruco_pose_display, aruco_detect_display


class ArucoPose(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.cal_ok = False
        self.K = None
        self.D = None

        row = QtWidgets.QHBoxLayout()
        self.intrinsic_cal_file_edit = PathEdit(mode="file", parent=self)
        self.intrinsic_cal_file_edit.acceptDrops()
        self.intrinsic_cal_file_edit.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.intrinsic_cal_file_edit.textChanged.connect(self.update_intrinsic_cal)
        self.intrinsic_cal_file_edit.setToolTip("Calibration file path.")
        row.addWidget(self.intrinsic_cal_file_edit)

        self.dir_button = QtWidgets.QPushButton(self)
        self.dir_button.setText("…")
        self.dir_button.setMaximumWidth(20)
        self.dir_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dir_button.clicked.connect(self.set_dir)
        self.dir_button.setToolTip("Get calibration file.")
        row.addWidget(self.dir_button)

        self.icon_size = 18
        self.cal_status_label = QtWidgets.QLabel(self)
        self.cross_icon = qta.icon("mdi.close-circle", color="red")
        self.tick_icon = qta.icon("mdi.check-circle", color="green")
        self.cal_status_label.setPixmap(self.cross_icon.pixmap(self.icon_size))
        self.cal_status_label.setToolTip("Calibration unsuccessful.")
        row.addWidget(self.cal_status_label)
        self.form_layout.addRow("Calibration File: ", row)

        self.aruco_set = QtWidgets.QComboBox(self)
        self.aruco_set.addItems(enum_aruco_dict.keys())
        self.form_layout.addRow("Aruco Set:", self.aruco_set)

        self.aruco_set.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def set_dir(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName()
        if file_name:
            self.intrinsic_cal_file_edit.setText(file_name)

    def set_cal_ok(self):
        self.cal_ok = True
        self.cal_status_label.setPixmap(self.tick_icon.pixmap(self.icon_size))
        self.cal_status_label.setToolTip("Calibration successful.")

    def set_cal_bad(self):
        self.cal_ok = False
        self.cal_status_label.setPixmap(self.cross_icon.pixmap(self.icon_size))
        self.cal_status_label.setToolTip("Calibration unsuccessful.")

    def update_intrinsic_cal(self):
        try:
            file_name = self.intrinsic_cal_file_edit.text()
            self.K, self.D = load_intrinsic(Path(file_name).resolve())
            self.set_cal_ok()
        except Exception as e:
            self.set_cal_bad()
        self.settings_updated.emit()

    def process_img(self, img):
        aruco_dict = cv.aruco.Dictionary_get(
            enum_aruco_dict[self.aruco_set.currentText()]
        )

        aruco_params = cv.aruco.DetectorParameters_create()
        corners, ids, rejected = cv.aruco.detectMarkers(
            img, aruco_dict, parameters=aruco_params
        )

        if len(corners) > 0 and img.ndim <= 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            if self.cal_ok:
                img = aruco_pose_display(corners, ids, img, self.K, self.D)
            else:
                img = aruco_detect_display(corners, ids, img)
        return img
