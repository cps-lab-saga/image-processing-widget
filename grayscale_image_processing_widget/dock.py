from grayscale_image_processing_widget.defs import QtCore, QtWidgets

from grayscale_image_processing_widget.groupboxes import (
    OrientGroupBox,
    PeekGroupBox,
    ProcessGroupBox,
    SaveGroupBox,
)


class ImgProcessDock(QtWidgets.QDockWidget):
    def __init__(self):
        super().__init__()

        self.dock_contents = QtWidgets.QFrame(self)
        self.setWidget(self.dock_contents)
        self.setTitleBarWidget(QtWidgets.QLabel(self))
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.setFeatures(
            self.DockWidgetFloatable | self.DockWidgetMovable | self.DockWidgetClosable
        )

        self.setObjectName("ImgProcessDock")

        self.dock_layout = QtWidgets.QVBoxLayout(self.dock_contents)

        self.process_groupbox = ProcessGroupBox(self.dock_contents)
        self.dock_layout.addWidget(self.process_groupbox)

        self.peek_groupbox = PeekGroupBox(self.dock_contents)
        self.dock_layout.addWidget(self.peek_groupbox)

        self.orient_groupbox = OrientGroupBox(self.dock_contents)
        self.dock_layout.addWidget(self.orient_groupbox)

        self.save_groupbox = SaveGroupBox(self.dock_contents)
        self.dock_layout.addWidget(self.save_groupbox)

    def connect_ui(self, update_func):
        self.process_groupbox.stacked_layout.currentChanged.connect(update_func)
        self.process_groupbox.connect_ui(update_func)
        self.orient_groupbox.connect_ui(update_func)

    def gui_save(self, settings):
        self.process_groupbox.gui_save(settings)
        self.orient_groupbox.gui_save(settings)
        self.save_groupbox.gui_save(settings)

    def gui_restore(self, settings):
        self.process_groupbox.gui_restore(settings)
        self.orient_groupbox.gui_restore(settings)
        self.save_groupbox.gui_restore(settings)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ImgProcessDock()
    widget.show()

    app.exec()
