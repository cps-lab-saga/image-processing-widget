from grayscale_image_processing_widget.defs import QtCore, QtWidgets, Signal


class DoubleSlider(QtWidgets.QSlider):
    doubleValueChanged = Signal(float)

    def __init__(self, *args, decimals=3, tip_offset=(0, -45), **kargs):
        super().__init__(*args, **kargs)
        self._multi = 10**decimals

        self.tip_offset = QtCore.QPoint(*tip_offset)

        self.style = QtWidgets.QApplication.style()
        self.opt = QtWidgets.QStyleOptionSlider()

        self.valueChanged.connect(self.emitDoubleValueChanged)
        self.sliderPressed.connect(self.show_tip)
        self.sliderMoved.connect(self.show_tip)

    def emitDoubleValueChanged(self):
        value = float(super().value()) / self._multi
        self.doubleValueChanged.emit(value)

    def value(self):
        return float(super().value()) / self._multi

    def setMinimum(self, value):
        return super().setMinimum(value * self._multi)

    def setMaximum(self, value):
        return super().setMaximum(value * self._multi)

    def setRange(self, min, max):
        return super().setRange(min * self._multi, max * self._multi)

    def setSingleStep(self, value):
        return super().setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super().singleStep()) / self._multi

    def setValue(self, value):
        super().setValue(int(value * self._multi))

    def show_tip(self):
        self.initStyleOption(self.opt)
        rectHandle = self.style.subControlRect(
            self.style.CC_Slider, self.opt, self.style.SC_SliderHandle
        )
        pos_local = rectHandle.topLeft() + self.tip_offset
        pos_global = self.mapToGlobal(pos_local)
        QtWidgets.QToolTip.showText(pos_global, f"{self.value()}", self)
