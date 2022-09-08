import contextlib

import pyqtgraph as pg

from image_processing_widget.defs import QtCore, QtWidgets


class RoiDataPlot(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        pg.setConfigOptions(
            background=None,
            foreground=self.palette().color(self.foregroundRole()),
            antialias=True,
        )

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.plot_widget = pg.PlotWidget()
        self.fig = self.plot_widget.getPlotItem()
        self.fig.setMenuEnabled(False)
        self.main_layout.addWidget(self.plot_widget)

        self.show_crosshairs = False
        self.crosshair_pen = pg.mkPen(color=(23, 190, 207), width=1)
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

    def set_data(self, data):
        pass

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
            self.v_crosshair.setPos(x)
            self.h_crosshair.setPos(y)
            xlim, ylim = self.fig.viewRange()
            self.v_crosshair_label.setText(str(x))
            self.v_crosshair_label.setPos(x, ylim[0])
            self.h_crosshair_label.setText(str(y))
            self.h_crosshair_label.setPos(xlim[0], y)

    def mouse_double_clicked(self, evt):
        """
        Double click right mouse button to toggle crosshairs
        """
        if not evt.double():
            return

        if evt.button() == QtCore.Qt.RightButton:
            if self.show_crosshairs:
                self.show_crosshairs = False
                self.fig.removeItem(self.v_crosshair)
                self.fig.removeItem(self.v_crosshair_label)
                self.fig.removeItem(self.h_crosshair)
                self.fig.removeItem(self.h_crosshair_label)
            else:
                self.show_crosshairs = True
                self.fig.addItem(self.v_crosshair, ignoreBounds=True)
                self.fig.addItem(self.v_crosshair_label, ignoreBounds=True)
                self.fig.addItem(self.h_crosshair, ignoreBounds=True)
                self.fig.addItem(self.h_crosshair_label, ignoreBounds=True)
                self.mouse_moved(evt.scenePos())

    def range_changed(self):
        """
        Move crosshair labels if resized.
        """
        if self.show_crosshairs:
            xlim, ylim = self.fig.viewRange()
            self.v_crosshair_label.setPos(self.v_crosshair_label.pos().x(), ylim[0])
            self.h_crosshair_label.setPos(xlim[0], self.h_crosshair_label.pos().y())
