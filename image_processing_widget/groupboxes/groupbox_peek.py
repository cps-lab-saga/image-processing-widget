import qtawesome as qta

from image_processing_widget.defs import QtCore, QtWidgets


class PeekGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(self.__class__.__name__)
        self.save_heading = self.__class__.__name__

        self.setTitle("Peek Original")
        main_layout = QtWidgets.QHBoxLayout(self)

        icon_size = 18
        peek_button = QtWidgets.QPushButton(self)
        peek_button.setIcon(qta.icon("mdi.image"))
        peek_button.setIconSize(QtCore.QSize(icon_size, icon_size))
        peek_button.setFlat(True)
        peek_button.setText("Hold to View")
        main_layout.addWidget(peek_button)

        self.peek_button = peek_button


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = PeekGroupBox()
    widget.show()

    app.exec()
