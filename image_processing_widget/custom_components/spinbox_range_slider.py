import logging

from superqt import QRangeSlider

from image_processing_widget.defs import QtCore, QtWidgets, Signal


class SpinBoxRangeSlider(QtWidgets.QWidget):
    valueChanged = Signal(float, float)
    valueChangeFinished = Signal(float, float)

    def __init__(self, *args, decimals=3, parent=None, unit="", **kargs):
        super().__init__(parent=parent)

        self._multi = 10**decimals
        self._decimals = decimals
        self._unit = unit
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.low_spinbox = QtWidgets.QDoubleSpinBox(self)
        self.low_spinbox.setSuffix(f" {unit}")
        self.low_spinbox.setDecimals(self._decimals)
        self.low_spinbox.valueChanged.connect(self._emit_valueChanged)
        self.low_spinbox.editingFinished.connect(self._emit_valueChangeFinished)
        layout.addWidget(self.low_spinbox)

        self.slider = QRangeSlider(*args, **kargs, parent=self)
        self.slider.valueChanged.connect(self._emit_valueChanged)
        self.slider.sliderReleased.connect(self._emit_valueChangeFinished)
        layout.addWidget(self.slider)

        self.high_spinbox = QtWidgets.QDoubleSpinBox(self)
        self.high_spinbox.setSuffix(f" {unit}")
        self.high_spinbox.setDecimals(self._decimals)
        self.high_spinbox.valueChanged.connect(self._emit_valueChanged)
        self.high_spinbox.editingFinished.connect(self._emit_valueChangeFinished)
        layout.addWidget(self.high_spinbox)

    def _emit_valueChanged(self):
        low, high = self._match_values(self.sender())
        self.valueChanged.emit(low, high)

    def _emit_valueChangeFinished(self):
        low, high = self._match_values(self.sender())
        self.valueChangeFinished.emit(low, high)

    def _match_values(self, sender):
        if sender == self.slider:
            low, high = (float(x) / self._multi for x in self.slider.value())

            low = self._fit_step(
                low, self.low_spinbox.minimum(), self.low_spinbox.singleStep()
            )
            self.low_spinbox.blockSignals(True)
            self.low_spinbox.setValue(low)
            self.low_spinbox.blockSignals(False)

            high = self._fit_step(
                high, self.high_spinbox.minimum(), self.high_spinbox.singleStep()
            )
            self.high_spinbox.blockSignals(True)
            self.high_spinbox.setValue(high)
            self.high_spinbox.blockSignals(False)

        else:
            low = self.low_spinbox.value()
            high = self.high_spinbox.value()
            if sender == self.low_spinbox and low > high:
                high = low
                self.high_spinbox.blockSignals(True)
                self.high_spinbox.setValue(high)
                self.high_spinbox.blockSignals(False)
            elif sender == self.high_spinbox and high < low:
                low = high
                self.low_spinbox.blockSignals(True)
                self.low_spinbox.setValue(low)
                self.low_spinbox.blockSignals(False)

            low = self._fit_step(
                low, self.low_spinbox.minimum(), self.low_spinbox.singleStep()
            )
            high = self._fit_step(
                high, self.high_spinbox.minimum(), self.high_spinbox.singleStep()
            )

            self.slider.blockSignals(True)
            self.slider.setValue((int(low * self._multi), int(high * self._multi)))
            self.slider.blockSignals(False)
        return low, high

    def _fit_step(self, val, min_val, step):
        mod = round((val - min_val) % step, self._decimals)
        if mod and mod != step:
            val -= mod
        return val

    def value(self):
        return (float(x) / self._multi for x in self.slider.value())

    def setMinimum(self, value):
        slider_min = round(value * self._multi)
        if slider_min < (-(2**31)):
            self._multi = (2**31 - 1) / value
            slider_min = round(value * self._multi)
            logging.warning(
                f"Invalid range! " f"Rescaled slider multiplier to {self._multi}"
            )
        self.slider.setMinimum(slider_min)
        self.low_spinbox.setMinimum(value)
        self.high_spinbox.setMinimum(value)

    def setMaximum(self, value):
        slider_max = round(value * self._multi)
        if slider_max > (2**31 - 1):
            self._multi = (2**31 - 1) / value
            slider_max = round(value * self._multi)
            logging.warning(
                f"Invalid range! " f"Rescaled slider multiplier to {self._multi}"
            )
        self.slider.setMaximum(slider_max)
        self.low_spinbox.setMaximum(value)
        self.high_spinbox.setMaximum(value)

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
        self.low_spinbox.setRange(min_value, max_value)
        self.high_spinbox.setRange(min_value, max_value)

    def setSingleStep(self, value):
        self.slider.setSingleStep(int(value * self._multi))
        self.low_spinbox.setSingleStep(value)
        self.high_spinbox.setSingleStep(value)

    def setValue(self, low, high):
        self.low_spinbox.setValue(low)
        self.high_spinbox.setValue(high)
        self.valueChangeFinished.emit(low, high)

    def singleStep(self):
        return float(self.slider.singleStep()) / self._multi


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = SpinBoxRangeSlider(orientation=QtCore.Qt.Horizontal)
    widget.setRange(0, 100)
    widget.setValue(0, 10)
    widget.show()

    app.exec()
