from image_processing_widget.custom_components import BaseDock
from image_processing_widget.defs import QtWidgets
from image_processing_widget.display_widget import HistogramWidget


class HistogramDock(BaseDock):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Histogram")

        self.histogram_widget = HistogramWidget()
        self.dock_layout.addWidget(self.histogram_widget)
        self.hide()

    def show_hide_dock(self, show):
        if show:
            self.show()
        else:
            self.hide()

    def set_data(self, histr):
        if type(histr) == dict:
            self.histogram_widget.set_rgb(histr)
        else:
            self.histogram_widget.set_grayscale(histr)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = HistogramDock()
    widget.show()

    app.exec()
