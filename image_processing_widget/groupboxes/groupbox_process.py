from image_processing_widget.custom_components import BaseGuiSave
from image_processing_widget.defs import QtWidgets, Signal


class ProcessGroupBox(QtWidgets.QGroupBox, BaseGuiSave):
    settings_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.setTitle("Operation")
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.process_plugins = []

        self.page_combo = QtWidgets.QComboBox(self)
        self.page_combo.activated.connect(self.switch_page)
        self.main_layout.addWidget(self.page_combo)

        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.currentChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.main_layout.addLayout(self.stacked_layout)

    def switch_page(self):
        self.stacked_layout.setCurrentIndex(self.page_combo.currentIndex())

    def add_process_plugin(self, name, plugin):
        self.page_combo.addItem(name)
        self.stacked_layout.addWidget(plugin)
        self.process_plugins.append(plugin)
        plugin.settings_updated.connect(self.settings_updated.emit)

    def adjust_range(self, size):
        for widget in self.process_plugins:
            widget.adjust_range(size)

    def gui_save(self, settings):
        super().gui_save(settings)
        for plugin in self.process_plugins:
            plugin.gui_save(settings)

    def gui_restore(self, settings):
        super().gui_restore(settings)
        for plugin in self.process_plugins:
            plugin.gui_restore(settings)
        self.switch_page()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widg = ProcessGroupBox()
    widg.show()

    app.exec()
