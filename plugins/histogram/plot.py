from image_processing_widget.custom_components import RoiDataPlot
from image_processing_widget.defs import QtWidgets


class HistogramPlot(RoiDataPlot):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.black_line = self.fig.plot(
            fillLevel=0, pen=(0, 0, 0), brush=(0, 0, 0, 50), name="Intensity"
        )
        self.red_line = self.fig.plot(
            fillLevel=0, pen=(255, 0, 0), brush=(255, 0, 0, 50), name="Red"
        )
        self.green_line = self.fig.plot(
            fillLevel=0, pen=(0, 255, 0), brush=(0, 255, 0, 50), name="Green"
        )
        self.blue_line = self.fig.plot(
            fillLevel=0, pen=(0, 0, 255), brush=(0, 0, 255, 50), name="Blue"
        )

    def set_data(self, histr):
        if isinstance(histr, dict):
            self._set_rgb(histr)
        else:
            self._set_grayscale(histr)

    def _set_rgb(self, histr):
        self.black_line.setData([0])
        self.red_line.setData(histr["r"])
        self.green_line.setData(histr["g"])
        self.blue_line.setData(histr["b"])

    def _set_grayscale(self, histr):
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
