import qtawesome as qta

from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtCore, QtWidgets, Signal


class SaveGroupBox(QtWidgets.QGroupBox, BaseGuiSave):
    save = Signal()
    save_as = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.setTitle("Save")
        self.main_layout = QtWidgets.QHBoxLayout(self)

        icon_size = 18
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setIcon(qta.icon("mdi.content-save"))
        self.save_button.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.save_button.setFlat(True)
        self.save_button.setToolTip("Save (Overwrite)")
        self.save_button.clicked.connect(self.save.emit)
        self.main_layout.addWidget(self.save_button)

        self.save_as_button = QtWidgets.QPushButton(self)
        self.save_as_button.setIcon(qta.icon("mdi.content-save-edit"))
        self.save_as_button.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.save_as_button.setFlat(True)
        self.save_as_button.setToolTip("Save As")
        self.save_as_button.clicked.connect(self.save_as.emit)
        self.main_layout.addWidget(self.save_as_button)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = SaveGroupBox()
    widget.show()

    app.exec()
