from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtWidgets


class ProcessBase(QtWidgets.QWidget, BaseGuiSave):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.form_layout = QtWidgets.QFormLayout(self)

    def connect_ui(self, update_func):
        pass

    def adjust_range(self, shape):
        pass

    def process_img(self, img):
        return img


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ProcessBase()
    widget.show()

    app.exec()
