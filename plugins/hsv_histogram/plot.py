import pyqtgraph as pg

from image_processing_widget.defs import QtWidgets


class HSVHistogramPlot(QtWidgets.QWidget):
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
        self.fig.addLegend()
        self.main_layout.addWidget(self.plot_widget)

        self.hue_line = self.fig.plot(
            fillLevel=0, pen=(255, 127, 14), brush=(255, 127, 14, 50), name="Hue"
        )
        self.sat_line = self.fig.plot(
            fillLevel=0,
            pen=(148, 103, 189),
            brush=(148, 103, 189, 50),
            name="Saturation",
        )
        self.val_line = self.fig.plot(
            fillLevel=0, pen=(188, 189, 34), brush=(188, 189, 34, 50), name="Value"
        )

    def set_data(self, histr):
        self.hue_line.setData(histr["h"])
        self.sat_line.setData(histr["s"])
        self.val_line.setData(histr["v"])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HSVHistogramPlot()
    widget.show()

    app.exec()
