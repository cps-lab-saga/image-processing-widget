from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtWidgets, Signal


class ImageModeGroupBox(QtWidgets.QGroupBox, BaseGuiSave):
    mode_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.mode = "grayscale"

        self.setTitle("Image Mode")
        self.main_layout = QtWidgets.QHBoxLayout(self)

        self.grayscale_button = QtWidgets.QRadioButton(self)
        self.grayscale_button.setText("Grayscale")
        self.grayscale_button.toggled.connect(self.mode_toggled)
        self.main_layout.addWidget(self.grayscale_button)

        self.color_button = QtWidgets.QRadioButton(self)
        self.color_button.setText("Color")
        self.color_button.toggled.connect(self.mode_toggled)
        self.main_layout.addWidget(self.color_button)

        self.grayscale_button.click()

    def mode_toggled(self):
        self.mode = self.sender().text().lower()
        self.mode_changed.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ImageModeGroupBox()
    widget.show()

    app.exec()
