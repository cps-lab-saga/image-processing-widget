from image_processing_widget.custom_components import BaseDock
from image_processing_widget.defs import QtWidgets
from .plot import HlacPlot


class HlacDock(BaseDock):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Higher Order Local Autocorrelation (HLAC)")

        self.hlac_plot = HlacPlot()
        self.dock_layout.addWidget(self.hlac_plot)
        self.hide()

    def show_hide_dock(self, show):
        if show:
            self.show()
        else:
            self.hide()

    def set_data(self, data):
        self.hlac_plot.set_feature_values(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HlacDock()
    widget.show()

    app.exec()
