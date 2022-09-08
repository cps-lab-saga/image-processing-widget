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
        self.peek_button = CustomButton(self)
        self.peek_button.setIcon(qta.icon("mdi.image"))
        self.peek_button.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.peek_button.setFlat(True)
        self.peek_button.setText("Hold to View")
        self.peek_button.started_press.connect(self.peek_started.emit)
        self.peek_button.stopped_press.connect(self.peek_ended.emit)
        self.main_layout.addWidget(self.peek_button)


class CustomButton(QtWidgets.QPushButton):
    started_press = Signal()
    stopped_press = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAutoRepeat(True)
        self.setAutoRepeatDelay(1000)
        self.setAutoRepeatInterval(1000)
        self.pressed.connect(self.button_pressed)
        self.released.connect(self.button_released)
        self._state = 0
        self._latch = 0

    def button_pressed(self):
        if self._latch == 0:
            if self._state == 0:
                self._state = 1
                self.started_press.emit()
            else:
                self._latch = 1
                self._state = 1
                self.setAutoRepeat(False)
        else:
            self._latch = 0
            self.setAutoRepeat(True)

    def button_released(self):
        if self._latch == 0:
            if self.isDown():
                return
            self._state = 0
            self.stopped_press.emit()
        else:
            self.setDown(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = PeekGroupBox()
    widget.show()

    app.exec()
