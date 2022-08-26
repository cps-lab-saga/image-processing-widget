import cv2 as cv
import numpy as np

from image_processing_widget.roi_plugin import RoiPlugin
from .dock import HlacDock
from .mask import mask


class HlacPlugin(RoiPlugin):
    def __init__(self):
        super().__init__()

        self.dock = HlacDock()
        self.kwargs = {}

    def roi_shown(self, show):
        self.dock.show_hide_dock(show)

    def roi_moved(self, img_slice):
        result = extract_hlac(img_slice)
        self.dock.set_data(result)


def extract_hlac(img):
    result = []
    for m in mask:
        feature_map = cv.filter2D(src=img, ddepth=-1, kernel=m)
        count = np.sum(feature_map == np.sum(m))
        result.append(count)
    return np.array(result)
