import logging

from image_processing_widget.defs import QtCore, QtWidgets, Signal


class MySlider(QtWidgets.QWidget):
    valueChanged = Signal(float)
    valueChangeFinished = Signal(float)

    def __init__(self, *args, decimals=3, parent=None, unit="", **kargs):
        super().__init__(parent=parent)

        self._multi = 10**decimals
        self._decimals = decimals
        self._unit = unit
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.slider = QtWidgets.QSlider(*args, **kargs, parent=self)
        self.slider.valueChanged.connect(self.emitValueChanged)
        self.slider.sliderReleased.connect(self.emitValueChangeFinished)

        self.spinbox = QtWidgets.QDoubleSpinBox(self)
        self.spinbox.setSuffix(f" {unit}")
        self.spinbox.setDecimals(self._decimals)
        self.spinbox.valueChanged.connect(self.emitValueChanged)
        self.spinbox.editingFinished.connect(self.emitValueChangeFinished)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.slider)

    def emitValueChanged(self):
        value = self.match_values(self.sender())
        self.valueChanged.emit(value)

    def emitValueChangeFinished(self):
        value = self.match_values(self.sender())
        self.valueChangeFinished.emit(value)

    def match_values(self, sender):
        if sender == self.slider:
            value = float(self.slider.value()) / self._multi
            mod = round(
                (value - self.spinbox.minimum()) % self.spinbox.singleStep(),
                self._decimals,
            )
            if mod and mod != self.spinbox.singleStep():
                value -= mod
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(value)
            self.spinbox.blockSignals(False)
        else:
            value = self.spinbox.value()
            mod = round(
                (value - self.spinbox.minimum()) % self.spinbox.singleStep(),
                self._decimals,
            )
            if mod and mod != self.spinbox.singleStep():
                value -= mod
            self.slider.blockSignals(True)
            self.slider.setValue(int(value * self._multi))
            self.slider.blockSignals(False)
        return value

    def value(self):
        return float(self.slider.value()) / self._multi

    def setMinimum(self, value):
        slider_min = round(value * self._multi)
        if slider_min < (-(2**31)):
            self._multi = (2**31 - 1) / value
            slider_min = round(value * self._multi)
            logging.warning(
                f"Invalid range! " f"Rescaled slider multiplier to {self._multi}"
            )
        self.slider.setMinimum(slider_min)
        self.spinbox.setMinimum(value)

    def setMaximum(self, value):
        slider_max = round(value * self._multi)
        if slider_max > (2**31 - 1):
            self._multi = (2**31 - 1) / value
            slider_max = round(value * self._multi)
            logging.warning(
                f"Invalid range! " f"Rescaled slider multiplier to {self._multi}"
            )
        self.slider.setMaximum(slider_max)
        self.spinbox.setMaximum(value)

    def setRange(self, min_value, max_value):
        slider_max = round(max_value * self._multi)
        slider_min = round(min_value * self._multi)

        if slider_min < (-(2**31)) or slider_max > (2**31 - 1):
            self._multi = (2**31 - 1) / max(abs(min_value), max_value)
            slider_max = round(max_value * self._multi)
            slider_min = round(min_value * self._multi)
            logging.warning(
                f"Invalid range! " f"Rescaled slider multiplier to {self._multi}"
            )

        self.slider.setRange(slider_min, slider_max)
        self.spinbox.setRange(min_value, max_value)

    def setSingleStep(self, value):
        self.slider.setSingleStep(int(value * self._multi))
        self.spinbox.setSingleStep(value)

    def setValue(self, value):
        self.slider.setValue(int(value * self._multi))
        self.spinbox.setValue(value)
        self.valueChangeFinished.emit(value)

    def singleStep(self):
        return float(self.slider.singleStep()) / self._multi


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MySlider(orientation=QtCore.Qt.Horizontal)
    widget.setRange(0, 2**31)
    widget.show()

    app.exec()
