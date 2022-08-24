from image_processing_widget.custom_components.gui_save_base import BaseGuiSave
from image_processing_widget.defs import QtWidgets, Signal


class ProcessGroupBox(QtWidgets.QGroupBox, BaseGuiSave):
    updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.setTitle("Operation")
        main_layout = QtWidgets.QVBoxLayout(self)

        self.process_widgets = []

        self.page_combo = QtWidgets.QComboBox(self)
        self.page_combo.activated.connect(self.switch_page)
        main_layout.addWidget(self.page_combo)

        self.stacked_layout = QtWidgets.QStackedLayout()
        main_layout.addLayout(self.stacked_layout)

    def switch_page(self):
        self.stacked_layout.setCurrentIndex(self.page_combo.currentIndex())

    def add_process(self, name, widget):
        self.page_combo.addItem(name)
        self.stacked_layout.addWidget(widget)
        self.process_widgets.append(widget)

    def connect_ui(self, update_func):
        for widget in self.process_widgets:
            widget.connect_ui(update_func)

    def adjust_range(self, size):
        for widget in self.process_widgets:
            widget.adjust_range(size)

    def gui_save(self, settings):
        super().gui_save(settings)
        for widget in self.process_widgets:
            widget.gui_save(settings)

    def gui_restore(self, settings):
        super().gui_restore(settings)
        for widget in self.process_widgets:
            widget.gui_restore(settings)
        self.switch_page()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widg = ProcessGroupBox()
    widg.show()

    app.exec()
