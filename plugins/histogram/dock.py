from image_processing_widget.custom_components import BaseDock
from image_processing_widget.defs import QtWidgets
from .plot import HistogramPlot


class HistogramDock(BaseDock):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Histogram")

        self.histogram_plot = HistogramPlot()
        self.dock_layout.addWidget(self.histogram_plot)
        self.hide()

    def show_hide_dock(self, show):
        if show:
            self.show()
        else:
            self.hide()

    def set_data(self, histr):
        if isinstance(histr, dict):
            self.histogram_plot._set_rgb(histr)
        else:
            self.histogram_plot._set_grayscale(histr)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HistogramDock()
    widget.show()

    app.exec()
