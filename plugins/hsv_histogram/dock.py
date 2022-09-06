from image_processing_widget.custom_components import BaseDock
from image_processing_widget.defs import QtWidgets
from .plot import HSVHistogramPlot


class HSVHistogramDock(BaseDock):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HSVHistogram")

        self.histogram_plot = HSVHistogramPlot()
        self.dock_layout.addWidget(self.histogram_plot)
        self.hide()

    def show_hide_dock(self, show):
        if show:
            self.show()
        else:
            self.hide()

    def set_data(self, histr):
        self.histogram_plot.set_data(histr)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HSVHistogramDock()
    widget.show()

    app.exec()
