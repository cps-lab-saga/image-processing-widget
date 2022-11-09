from image_processing_widget.custom_components import BaseDock
from image_processing_widget.defs import QtWidgets, Signal
from image_processing_widget.groupboxes import (
    ImageModeGroupBox,
    OrientGroupBox,
    PeekGroupBox,
    ProcessGroupBox,
    SaveGroupBox,
)


class ControlsDock(BaseDock):
    mode_changed = Signal()
    settings_updated = Signal()
    peek_started = Signal()
    peek_ended = Signal()
    save = Signal()
    save_as = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controls")
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.image_mode_groupbox = ImageModeGroupBox(self.dock_contents)
        self.image_mode_groupbox.mode_changed.connect(self.mode_changed.emit)
        self.dock_layout.addWidget(self.image_mode_groupbox)

        self.process_groupbox = ProcessGroupBox(self.dock_contents)
        self.process_groupbox.settings_updated.connect(self.settings_updated.emit)
        self.dock_layout.addWidget(self.process_groupbox)

        self.peek_groupbox = PeekGroupBox(self.dock_contents)
        self.peek_groupbox.peek_started.connect(self.peek_started.emit)
        self.peek_groupbox.peek_ended.connect(self.peek_ended.emit)
        self.dock_layout.addWidget(self.peek_groupbox)

        self.orient_groupbox = OrientGroupBox(self.dock_contents)
        self.orient_groupbox.settings_updated.connect(self.settings_updated.emit)
        self.dock_layout.addWidget(self.orient_groupbox)

        self.save_groupbox = SaveGroupBox(self.dock_contents)
        self.save_groupbox.save.connect(self.save.emit)
        self.save_groupbox.save_as.connect(self.save_as.emit)
        self.dock_layout.addWidget(self.save_groupbox)

    def gui_save(self, settings):
        self.image_mode_groupbox.gui_save(settings)
        self.process_groupbox.gui_save(settings)
        self.orient_groupbox.gui_save(settings)
        self.save_groupbox.gui_save(settings)

    def gui_restore(self, settings):
        self.image_mode_groupbox.gui_restore(settings)
        self.process_groupbox.gui_restore(settings)
        self.orient_groupbox.gui_restore(settings)
        self.save_groupbox.gui_restore(settings)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ControlsDock()
    widget.show()

    app.exec()
