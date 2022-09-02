from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtWidgets, Signal


class ProcessPlugin(QtWidgets.QWidget, BaseGuiSave):
    settings_updated = Signal()
    process_failed = Signal(str)

    def __init__(self):
        super().__init__()

        self.dock = None

        self.name = self.__class__.__name__
        self.setObjectName(self.name)
        self.save_heading = f"Plugin.{self.name}"

        self.form_layout = QtWidgets.QFormLayout(self)

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        return img
