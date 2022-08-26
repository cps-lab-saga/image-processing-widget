import cv2 as cv

from image_processing_widget.roi_plugin import RoiPlugin
from .dock import HistogramDock


class HistogramPlugin(RoiPlugin):
    def __init__(self):
        super().__init__()

        self.dock = HistogramDock()
        self.kwargs = {}

    def roi_shown(self, show):
        self.dock.show_hide_dock(show)

    def roi_moved(self, img_slice):
        histr = calculate_histogram(img_slice)
        self.dock.set_data(histr)


def calculate_histogram(img_slice):
    if img_slice.ndim == 3:
        histr = {
            color: cv.calcHist(
                images=[img_slice],
                channels=[i],
                mask=None,
                histSize=[2**8],
                ranges=[0, 2**8],
            ).flat
            for i, color in enumerate(("r", "g", "b"))
        }
        return histr

    elif img_slice.ndim == 2:
        histr = cv.calcHist(
            images=[img_slice],
            channels=[0],
            mask=None,
            histSize=[2**8],
            ranges=[0, 2**8],
        ).flat
        return histr
