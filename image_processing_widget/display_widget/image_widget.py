import contextlib

import pyqtgraph as pg

from image_processing_widget.defs import QtCore, QtWidgets, DisplayMode


class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.img = None

        self.setToolTip("Drop images here.")
        self.display_mode = DisplayMode.AUTO

        pg.setConfigOptions(
            background=None,
            foreground=self.palette().color(self.foregroundRole()),
            antialias=True,
        )

        self.show_crosshairs = False
        self.crosshair_pen = pg.mkPen(color=(23, 190, 207), width=1)

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

    def setImage(self, img):
        self.img = img
        if self.display_mode == DisplayMode.AUTO:
            self.im_item.setImage(img)
        elif self.display_mode == DisplayMode.BIT12:
            self.im_item.setImage(img, levels=(0, 2**12 - 1))
        elif self.display_mode == DisplayMode.BIT16:
            self.im_item.setImage(img, levels=(0, 2**16 - 1))

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
        if evt.double() and evt.button() == QtCore.Qt.RightButton:
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

    def range_changed(self):
        """
        Move crosshair labels if resized.
        """
        if self.show_crosshairs:
            xlim, ylim = self.fig.viewRange()
            self.v_crosshair_label.setPos(self.v_crosshair_label.pos().x(), ylim[1])
            self.h_crosshair_label.setPos(xlim[0], self.h_crosshair_label.pos().y())
            self.intensity_crosshair_label.setPos(xlim[1], ylim[0])


if __name__ == "__main__":
    import numpy as np

    black_img = np.zeros([100, 100, 3], dtype=np.uint8)

    app = QtWidgets.QApplication([])
    widget = ImageWidget()
    widget.imv.setImage(black_img)
    widget.show()

    app.exec()
