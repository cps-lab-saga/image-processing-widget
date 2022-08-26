from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtCore, Signal


class RoiPlugin(QtCore.QObject, BaseGuiSave):
    settings_updated = Signal()

    def __init__(self):
        super().__init__()

        self.dock = None

        self.name = self.__class__.__name__
        self.setObjectName(self.name)
        self.save_heading = f"Plugin.{self.name}"

    def roi_shown(self, show):
        pass

    def roi_moved(self, img_slice):
        pass
