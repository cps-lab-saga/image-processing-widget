import pyqtgraph as pg

from image_processing_widget.custom_components import RoiDataPlot
from image_processing_widget.defs import QtWidgets
from .mask import mask


class HlacPlot(RoiDataPlot):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        x = range(1, len(mask) + 1)

        self.bargraph = pg.BarGraphItem(x=x, height=[0] * len(x), width=0.8, brush="k")

        self.fig.addItem(self.bargraph)
        self.fig.setLabel("left", "Feature Value")
        self.fig.setLabel("bottom", "HLAC Features")
        self.fig.getAxis("bottom").setTicks([[(i, str(i)) for i in x]])

    def set_data(self, feature_values):
        self.bargraph.setOpts(height=feature_values)


if __name__ == "__main__":
    import numpy as np

    sample_data = np.array(range(25))

    app = QtWidgets.QApplication([])
    widget = HlacPlot()
    widget.set_data(sample_data)
    widget.show()

    app.exec()
