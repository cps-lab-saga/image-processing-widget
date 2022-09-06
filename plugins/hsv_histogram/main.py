import cv2 as cv

from image_processing_widget.roi_plugin import RoiPlugin
from .dock import HSVHistogramDock


class HSVHistogramPlugin(RoiPlugin):
    def __init__(self):
        super().__init__()

        self.dock = HSVHistogramDock()
        self.kwargs = {}

    def roi_shown(self, show):
        self.dock.show_hide_dock(show)

    def roi_moved(self, img_slice):
        histr = calculate_hsv_histogram(img_slice)
        self.dock.set_data(histr)


def calculate_hsv_histogram(img_slice):
    if img_slice.ndim == 2:
        img_slice = cv.cvtColor(img_slice, cv.COLOR_GRAY2BGR)
    hsv = cv.cvtColor(img_slice, cv.COLOR_BGR2HSV)
    return {
        color: cv.calcHist(
            images=[hsv], channels=[i], mask=None, histSize=[2**8], ranges=[0, 2**8]
        ).flat
        for i, color in enumerate(("h", "s", "v"))
    }
