from image_processing_widget.custom_components import RoiDataPlot
from image_processing_widget.defs import QtWidgets


class HSVHistogramPlot(RoiDataPlot):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.fig.setLabel("left", "Frequency")
        self.fig.setLabel("bottom", "Intensity")

        self.fig.addLegend()
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
