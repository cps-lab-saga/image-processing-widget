import contextlib
import logging

import numpy as np
import pyqtgraph as pg

from image_processing_widget.defs import QtCore, QtWidgets, Signal, DisplayMode


class ImageWidget(QtWidgets.QWidget):
    slice_selected = Signal(bool)
    slice_selection_changed = Signal(np.ndarray)

    def __init__(self, config_parser=None, parent=None):
        super().__init__(parent=parent)

        self.img = None

        self.setToolTip("Drop images here.")
        self.display_mode = DisplayMode.AUTO

        self.config = self.get_image_config(config_parser)

        pg.setConfigOptions(
            background=None,
            foreground=self.palette().color(self.foregroundRole()),
            antialias=True,
        )

        self.show_crosshairs = False
        self.show_roi = False
        self.crosshair_pen = pg.mkPen(color=(23, 190, 207), width=1)
        self.roi_pen = pg.mkPen(color=(44, 160, 44), width=2)
        self.roi_hover_pen = pg.mkPen(color=(188, 189, 34), width=2)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.plot_widget = pg.PlotWidget()
        self.fig = self.plot_widget.getPlotItem()
        self.main_layout.addWidget(self.plot_widget)

        self.im_item = pg.ImageItem(axisOrder="row-major")

        self.fig.addItem(self.im_item)
        self.fig.setAspectLocked()
        self.fig.invertY(True)
        self.fig.setMenuEnabled(False)
        # fig.hideAxis('left')
        # fig.hideAxis('bottom')

        self.v_crosshair = pg.InfiniteLine(
            pos=pg.Point(-1000, -1000), angle=90, movable=False, pen=self.crosshair_pen
        )
        self.v_crosshair_label = pg.TextItem(
            "", anchor=(0, 1), color=self.crosshair_pen.color(), fill=(0, 0, 0)
        )
        self.h_crosshair = pg.InfiniteLine(
            pos=pg.Point(-1000, -1000), angle=0, movable=False, pen=self.crosshair_pen
        )
        self.h_crosshair_label = pg.TextItem(
            "", anchor=(0, 1), color=self.crosshair_pen.color(), fill=(0, 0, 0)
        )
        self.intensity_crosshair_label = pg.TextItem(
            "", anchor=(1, 0), color=self.crosshair_pen.color(), fill=(0, 0, 0)
        )

        self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)
        self.plot_widget.sigRangeChanged.connect(self.range_changed)
        self.plot_widget.scene().sigMouseClicked.connect(self.mouse_double_clicked)

        self.roi = pg.ROI(
            (0, 0),
            size=(20, 20),
            pen=self.roi_pen,
            hoverPen=self.roi_hover_pen,
            movable=True,
            resizable=True,
            rotatable=False,
            rotateSnap=False,
            scaleSnap=True,
        )
        self.roi.addScaleHandle((1, 1), (0.5, 0.5))
        self.roi.sigRegionChanged.connect(self.roi_moved)

    def set_image(self, img):
        self.img = img
        if self.display_mode == DisplayMode.AUTO:
            self.im_item.setImage(img)
        elif self.display_mode == DisplayMode.BIT8:
            self.im_item.setImage(img, levels=(0, 2**8))
        self.range_changed()

    def mouse_moved(self, pos):
        """
        animate crosshairs and display x and y values
        """
        if not self.fig.sceneBoundingRect().contains(pos) or not self.show_crosshairs:
            return

        with contextlib.suppress(Exception):
            mouse_point = self.fig.vb.mapSceneToView(pos)
            x = round(mouse_point.x())
            y = round(mouse_point.y())
            intensity = self.img[y, x]
            self.v_crosshair.setPos(x)
            self.h_crosshair.setPos(y)
            xlim, ylim = self.fig.viewRange()
            self.v_crosshair_label.setText(str(x))
            self.v_crosshair_label.setPos(x, ylim[1])
            self.h_crosshair_label.setText(str(y))
            self.h_crosshair_label.setPos(xlim[0], y)
            self.intensity_crosshair_label.setText(str(intensity))
            self.intensity_crosshair_label.setPos(xlim[1], ylim[0])

    def mouse_double_clicked(self, evt):
        """
        Double click right mouse button to toggle crosshairs
        """
        if not evt.double() or self.img is None:
            return

        if evt.button() == QtCore.Qt.RightButton:
            if self.show_crosshairs:
                self.show_crosshairs = False
                self.fig.removeItem(self.v_crosshair)
                self.fig.removeItem(self.v_crosshair_label)
                self.fig.removeItem(self.h_crosshair)
                self.fig.removeItem(self.h_crosshair_label)
                self.fig.removeItem(self.intensity_crosshair_label)
            else:
                self.show_crosshairs = True
                self.fig.addItem(self.v_crosshair, ignoreBounds=True)
                self.fig.addItem(self.v_crosshair_label, ignoreBounds=True)
                self.fig.addItem(self.h_crosshair, ignoreBounds=True)
                self.fig.addItem(self.h_crosshair_label, ignoreBounds=True)
                self.fig.addItem(self.intensity_crosshair_label, ignoreBounds=True)
                self.mouse_moved(evt.scenePos())

        elif evt.button() == QtCore.Qt.LeftButton:
            if self.show_roi:
                self.show_roi = False
                self.fig.removeItem(self.roi)
            else:
                mouse_point = self.fig.vb.mapSceneToView(evt.scenePos())
                x = round(mouse_point.x())
                y = round(mouse_point.y())
                wx = int(self.img.shape[1] * 0.1)
                wy = int(self.img.shape[0] * 0.1)

                self.roi.setPos((x - wx / 2, y - wy / 2))
                self.roi.setSize((wx, wy))
                self.roi.setAngle(0)

                self.show_roi = True
                self.fig.addItem(self.roi)
                self.mouse_moved(evt.scenePos())

            self.slice_selected.emit(self.show_roi)

    def range_changed(self):
        """
        Move crosshair labels if resized.
        """
        if self.show_crosshairs:
            xlim, ylim = self.fig.viewRange()
            self.v_crosshair_label.setPos(self.v_crosshair_label.pos().x(), ylim[1])
            self.h_crosshair_label.setPos(xlim[0], self.h_crosshair_label.pos().y())
            self.intensity_crosshair_label.setPos(xlim[1], ylim[0])

        if self.show_roi:
            self.roi_moved()

    def roi_moved(self):
        """
        keep roi inside image and as int and emit slice of image.
        """
        if self.img is None:
            return

        x, y, wx, wy = self.get_roi_rect()
        img_wy, img_wx = self.img.shape[:2]

        if wx > img_wx:
            wx = img_wx - 1
        if wy > img_wy:
            wy = img_wy - 1

        if x < 0:
            x = 0
        elif x + wx >= img_wx:
            x = img_wx - wx - 1
        if y < 0:
            y = 0
        elif y + wy >= img_wy:
            y = img_wy - wy - 1

        self.roi.blockSignals(True)
        self.roi.setPos((x, y))
        self.roi.setSize((wx, wy))
        self.roi.blockSignals(False)

        if self.img.ndim == 3:
            img_slice = self.img[y : y + wy, x : x + wx, :]
            self.slice_selection_changed.emit(img_slice)
        elif self.img.ndim == 2:
            img_slice = self.img[y : y + wy, x : x + wx]
            self.slice_selection_changed.emit(img_slice)

    def get_roi_rect(self):
        x, y = [round(c) for c in self.roi.pos()]
        wx, wy = [round(c) for c in self.roi.size()]
        return x, y, wx, wy

    @staticmethod
    def get_image_config(config_parser):
        config = {"display_mode": DisplayMode.AUTO}
        if config_parser is None:
            return config

        if config_parser.has_option("Image Config", "display_mode"):
            display_mode = config_parser.get("Image Config", "display_mode").strip()
            if display_mode.upper() == "AUTO":
                logging.info(f"display_mode: {display_mode}")
                config["display_mode"] = DisplayMode.AUTO
            elif display_mode.upper() in ["8BIT", "8-BIT"]:
                logging.info(f"display_mode: {display_mode}")
                config["display_mode"] = DisplayMode.BIT8
            else:
                logging.warning(f"Invalid display_mode: {display_mode}")

        return DisplayMode.AUTO


if __name__ == "__main__":
    import numpy as np

    black_img = np.zeros([100, 100, 3], dtype=np.uint8)

    app = QtWidgets.QApplication([])
    widget = ImageWidget()
    widget.imv.set_image(black_img)
    widget.show()

    app.exec()
