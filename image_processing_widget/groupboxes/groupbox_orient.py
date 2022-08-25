from itertools import cycle

import cv2 as cv
import qtawesome as qta

from image_processing_widget.custom_components import (
    BadgeButton,
    BaseGuiSave,
    tab10_qcolor,
)
from image_processing_widget.defs import QtCore, QtWidgets, Signal


class OrientGroupBox(QtWidgets.QGroupBox, BaseGuiSave):
    settings_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.setTitle("Orientation")
        self.main_layout = QtWidgets.QHBoxLayout(self)

        self.rot_cycle = cycle(["0", "90", "180", "270"])
        self.flip_cycle = cycle(["no_flip", "h_flip", "v_flip", "hv_flip"])
        self.rotation = next(self.rot_cycle)
        self.flip = next(self.flip_cycle)

        self.main_layout.addStretch()

        self.icon_size = 30
        self.badge_size = 8
        self.rotate_button = BadgeButton(
            self.badge_size, tab10_qcolor["red"], "white", self
        )
        self.rotate_icons = {
            "0": qta.icon("mdi.rotate-right", rotated=0),
            "90": qta.icon("mdi.rotate-right", rotated=90),
            "180": qta.icon("mdi.rotate-right", rotated=180),
            "270": qta.icon("mdi.rotate-right", rotated=270),
        }
        self.rotate_tooltips = {
            "0": "Rotate frame.",
            "90": "Rotated by 90 degrees.",
            "180": "Rotated by 180 degrees.",
            "270": "Rotated by 270 degrees.",
        }
        self.rotate_button.setIcon(self.rotate_icons[self.rotation])
        self.rotate_button.setToolTip(self.rotate_tooltips[self.rotation])
        self.rotate_button.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.rotate_button.setFlat(True)
        self.rotate_button.set_no_badge()
        self.main_layout.addWidget(self.rotate_button)
        self.rotate_button.clicked.connect(self.rotate_button_clicked)

        self.main_layout.addStretch()

        self.arrow_label = QtWidgets.QLabel(self)
        self.arrow_label.setPixmap(
            qta.icon("mdi.arrow-right", color="gray").pixmap(self.icon_size)
        )
        self.main_layout.addWidget(self.arrow_label)

        self.main_layout.addStretch()

        self.flip_button = BadgeButton(
            self.badge_size, tab10_qcolor["blue"], "white", self
        )
        self.flip_icons = {
            "no_flip": qta.icon("mdi.card-outline"),
            "h_flip": qta.icon("mdi.reflect-horizontal"),
            "v_flip": qta.icon("mdi.reflect-vertical"),
            "hv_flip": qta.icon(
                "mdi.reflect-horizontal",
                "mdi.reflect-vertical",
                options=[
                    {"scale_factor": 0.7, "offset": (-0.2, 0)},
                    {"scale_factor": 0.7, "offset": (0.2, 0)},
                ],
            ),
        }
        self.flip_tooltips = {
            "no_flip": "Flip frame.",
            "h_flip": "Flipped horizontally.",
            "v_flip": "Flipped vertically.",
            "hv_flip": "Flipped horizontally and vertically.",
        }

        self.flip_button.setIcon(self.flip_icons[self.flip])
        self.flip_button.setToolTip(self.flip_tooltips[self.flip])
        self.flip_button.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.flip_button.setFlat(True)
        self.flip_button.set_no_badge()
        self.main_layout.addWidget(self.flip_button)
        self.flip_button.clicked.connect(self.flip_button_clicked)

        self.main_layout.addStretch()

    def rotate_button_clicked(self):
        self.rotation = next(self.rot_cycle)
        self.update_rotate_button()
        self.settings_updated.emit()

    def update_rotate_button(self):
        self.rotate_button.setIcon(self.rotate_icons[self.rotation])
        self.rotate_button.setToolTip(self.rotate_tooltips[self.rotation])
        if self.rotation == "0":
            self.rotate_button.set_no_badge()
        else:
            self.rotate_button.set_badge(self.rotation)

    def flip_button_clicked(self):
        self.flip = next(self.flip_cycle)
        self.update_flip_button()
        self.settings_updated.emit()

    def update_flip_button(self):
        self.flip_button.setIcon(self.flip_icons[self.flip])
        self.flip_button.setToolTip(self.flip_tooltips[self.flip])
        if self.flip == "no_flip":
            self.flip_button.set_no_badge()
        else:
            self.flip_button.set_badge("✱")

    def rotate_img(self, img):
        settings = self.rotation
        if settings == "0":
            return img
        elif settings == "90":
            return cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
        elif settings == "180":
            return cv.rotate(img, cv.ROTATE_180)
        elif settings == "270":
            return cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)

    def flip_img(self, img):
        settings = self.flip
        if settings == "no_flip":
            return img
        elif settings == "h_flip":
            return cv.flip(img, 1)
        elif settings == "v_flip":
            return cv.flip(img, 0)
        elif settings == "hv_flip":
            return cv.flip(img, -1)

    def orient_img(self, img):
        return self.flip_img(self.rotate_img(img))

    def gui_save(self, settings):
        super().gui_save(settings)
        settings.setValue("Gui/rotate_settings", self.rotation)
        settings.setValue("Gui/flip_settings", self.flip)

    def gui_restore(self, settings):
        super().gui_restore(settings)
        rotation = settings.value("Gui/rotate_settings")
        if rotation in self.rotate_icons.keys():
            while self.rotation != rotation:
                self.rotation = next(self.rot_cycle)
            self.update_rotate_button()

        flip = settings.value("Gui/flip_settings")
        if flip in self.flip_icons.keys():
            while self.flip != flip:
                self.flip = next(self.flip_cycle)
            self.update_flip_button()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = OrientGroupBox()
    widget.show()

    app.exec()
