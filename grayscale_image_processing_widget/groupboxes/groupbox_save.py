import qtawesome as qta

from grayscale_image_processing_widget.custom_components.gui_save_base import (
    GuiSaveBase,
)
from grayscale_image_processing_widget.defs import QtCore, QtWidgets


class SaveGroupBox(QtWidgets.QGroupBox, GuiSaveBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setTitle("Save")
        main_layout = QtWidgets.QHBoxLayout(self)

        icon_size = 18
        save_button = QtWidgets.QPushButton(self)
        save_button.setIcon(qta.icon("mdi.content-save"))
        save_button.setIconSize(QtCore.QSize(icon_size, icon_size))
        save_button.setFlat(True)
        save_button.setToolTip("Save (Overwrite)")
        main_layout.addWidget(save_button)

        save_as_button = QtWidgets.QPushButton(self)
        save_as_button.setIcon(qta.icon("mdi.content-save-edit"))
        save_as_button.setIconSize(QtCore.QSize(icon_size, icon_size))
        save_as_button.setFlat(True)
        save_as_button.setToolTip("Save As")
        main_layout.addWidget(save_as_button)

        self.save_button = save_button
        self.save_as_button = save_as_button


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = SaveGroupBox()
    widget.show()

    app.exec()
