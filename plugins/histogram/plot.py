import pyqtgraph as pg

from image_processing_widget.defs import QtWidgets


class HistogramPlot(QtWidgets.QWidget):
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

        self.black_line = self.fig.plot(fillLevel=0, pen=(0, 0, 0), brush=(0, 0, 0, 50))
        self.red_line = self.fig.plot(
            fillLevel=0, pen=(255, 0, 0), brush=(255, 0, 0, 50)
        )
        self.green_line = self.fig.plot(
            fillLevel=0, pen=(0, 255, 0), brush=(0, 255, 0, 50)
        )
        self.blue_line = self.fig.plot(
            fillLevel=0, pen=(0, 0, 255), brush=(0, 0, 255, 50)
        )

    def set_rgb(self, histr):
        self.black_line.setData([0])
        self.red_line.setData(histr["r"])
        self.green_line.setData(histr["g"])
        self.blue_line.setData(histr["b"])

    def set_grayscale(self, histr):
        self.black_line.setData(histr)
        self.red_line.setData([0])
        self.green_line.setData([0])
        self.blue_line.setData([0])


if __name__ == "__main__":
    import numpy as np

    sample_data = np.array(range(25))

    app = QtWidgets.QApplication([])
    widget = HistogramPlot()
    widget.black_line.setData(sample_data)
    widget.show()

    app.exec()
