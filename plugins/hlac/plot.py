import pyqtgraph as pg

from image_processing_widget.defs import QtWidgets
from .mask import mask


class HlacPlot(QtWidgets.QWidget):
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

        x = range(1, len(mask) + 1)

        self.bargraph = pg.BarGraphItem(x=x, height=[0] * len(x), width=0.8, brush="k")

        self.fig.addItem(self.bargraph)
        self.fig.setLabel("left", "Feature Value")
        self.fig.setLabel("bottom", "HLAC Features")
        self.fig.getAxis("bottom").setTicks([[(i, str(i)) for i in x]])

    def set_feature_values(self, feature_values):
        self.bargraph.setOpts(height=feature_values)


if __name__ == "__main__":
    import numpy as np

    sample_data = np.array(range(25))

    app = QtWidgets.QApplication([])
    widget = HLACFeaturesWidget()
    widget.set_feature_values(sample_data)
    widget.show()

    app.exec()
