from grayscale_image_processing_widget.custom_components import GuiSaveBase
from grayscale_image_processing_widget.defs import QtWidgets, Signal
from grayscale_image_processing_widget.process_widgets import (
    BrightnessContrasts,
    MorphEx,
    Blur,
    Gradients,
    Thresholds,
    InRange,
    Canny,
    DetectLines,
    DetectCircles,
    FindContours,
    FitBoundary,
)


class ProcessGroupBox(QtWidgets.QGroupBox, GuiSaveBase):
    updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setTitle("Operation")
        main_layout = QtWidgets.QVBoxLayout(self)

        self.process_widgets = []

        self.page_combo = QtWidgets.QComboBox(self)
        self.page_combo.activated.connect(self.switch_page)
        main_layout.addWidget(self.page_combo)

        self.stacked_layout = QtWidgets.QStackedLayout()
        main_layout.addLayout(self.stacked_layout)

        self.add_process("Brightness & Contrasts", BrightnessContrasts(self))
        self.add_process("Blur", Blur(self))
        self.add_process("MorphEx", MorphEx(self))
        self.add_process("Gradients", Gradients(self))
        self.add_process("Thresholds", Thresholds(self))
        self.add_process("InRange", InRange(self))
        self.add_process("Canny Edge Detection", Canny(self))
        self.add_process("Detect Lines", DetectLines(self))
        self.add_process("Detect Circles", DetectCircles(self))
        self.add_process("Find Contours", FindContours(self))
        self.add_process("Fit Boundary", FitBoundary(self))

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
