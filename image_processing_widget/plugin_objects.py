from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtWidgets


class ProcessPlugin(QtWidgets.QWidget, BaseGuiSave):
    def __init__(self):
        super().__init__()

        self.dock = None

        self.name = self.__class__.__name__
        self.setObjectName(self.name)

        self.form_layout = QtWidgets.QFormLayout(self)

    def connect_ui(self, update_func):
        pass

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        return img
