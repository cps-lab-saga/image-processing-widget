import pyqtgraph as pg

from grayscale_image_processing_widget.defs import QtWidgets


class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.colormap = "grey"
        self.setToolTip("Drop images here.")

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
        self.im_item.setImage(img)


if __name__ == "__main__":
    import numpy as np

    black_img = np.zeros([100, 100, 3], dtype=np.uint8)

    app = QtWidgets.QApplication([])
    widget = ImageWidget()
    widget.imv.setImage(black_img)
    widget.show()

    app.exec()
