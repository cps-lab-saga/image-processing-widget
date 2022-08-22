import pyqtgraph as pg

from image_processing_widget.defs import QtWidgets, DisplayMode


class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.colormap = "grey"
        self.setToolTip("Drop images here.")
        self.display_mode = DisplayMode.AUTO

        pg.setConfigOptions(
            background=None,
            foreground=self.palette().color(self.foregroundRole()),
            antialias=True,
        )

        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)

        plot_widget = pg.PlotWidget()
        fig = plot_widget.getPlotItem()
        layout.addWidget(plot_widget)

        im_item = pg.ImageItem(axisOrder="row-major")

        fig.addItem(im_item)
        fig.setAspectLocked()
        fig.invertY(True)
        fig.setMenuEnabled(False)
        # fig.hideAxis('left')
        # fig.hideAxis('bottom')

        self.im_item = im_item
        self.fig = fig

    def setImage(self, img):
        if self.display_mode == DisplayMode.AUTO:
            self.im_item.setImage(img)
        elif self.display_mode == DisplayMode.BIT12:
            self.im_item.setImage(img, levels=(0, 2**12 - 1))
        elif self.display_mode == DisplayMode.BIT16:
            self.im_item.setImage(img, levels=(0, 2**16 - 1))


if __name__ == "__main__":
    import numpy as np

    black_img = np.zeros([100, 100, 3], dtype=np.uint8)

    app = QtWidgets.QApplication([])
    widget = ImageWidget()
    widget.imv.setImage(black_img)
    widget.show()

    app.exec()
