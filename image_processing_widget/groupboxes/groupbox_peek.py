import qtawesome as qta

from image_processing_widget.defs import QtCore, QtWidgets, Signal


class PeekGroupBox(QtWidgets.QGroupBox):
    peek_started = Signal()
    peek_ended = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.setTitle("Peek Original")
        self.main_layout = QtWidgets.QHBoxLayout(self)

        self.icon_size = 18
        self.peek_button = QtWidgets.QPushButton(self)
        self.peek_button.setIcon(qta.icon("mdi.image"))
        self.peek_button.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.peek_button.setFlat(True)
        self.peek_button.setText("Hold to View")
        self.peek_button.pressed.connect(self.peek_started.emit)
        self.peek_button.released.connect(self.peek_ended.emit)
        self.main_layout.addWidget(self.peek_button)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = PeekGroupBox()
    widget.show()

    app.exec()
