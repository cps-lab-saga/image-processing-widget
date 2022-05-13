import inspect
from distutils.util import strtobool

from grayscale_image_processing_widget.custom_components.double_slider import DoubleSlider
from grayscale_image_processing_widget.defs import QtWidgets


class GuiSaveBase:
    def gui_save(self, settings):
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QtWidgets.QLineEdit):
                value = obj.text()
                settings.setValue("Gui/" + name, value)
            elif isinstance(obj, QtWidgets.QSpinBox):
                value = obj.value()
                settings.setValue("Gui/" + name, value)
            elif isinstance(obj, QtWidgets.QDoubleSpinBox):
                value = obj.value()
                settings.setValue("Gui/" + name, value)
            elif isinstance(obj, QtWidgets.QRadioButton):
                state = obj.isChecked()
                settings.setValue("Gui/" + name, state)
            elif isinstance(obj, QtWidgets.QCheckBox):
                state = obj.isChecked()
                settings.setValue("Gui/" + name, state)
            elif isinstance(obj, QtWidgets.QPushButton):
                if obj.isCheckable():
                    state = obj.isChecked()
                    settings.setValue("Gui/" + name, state)
            elif isinstance(obj, QtWidgets.QComboBox):
                value = obj.currentText()
                settings.setValue("Gui/" + name, value)
            elif isinstance(obj, DoubleSlider):
                value = obj.value()
                settings.setValue("Gui/" + name, value)

    def gui_restore(self, settings):
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QtWidgets.QLineEdit):
                if settings.value("Gui/" + name) is not None:
                    value = settings.value("Gui/" + name)
                    obj.setText(value)
            elif isinstance(obj, QtWidgets.QSpinBox):
                if settings.value("Gui/" + name) is not None:
                    value = int(settings.value("Gui/" + name))
                    obj.setValue(value)
            elif isinstance(obj, QtWidgets.QDoubleSpinBox):
                if settings.value("Gui/" + name) is not None:
                    value = float(settings.value("Gui/" + name))
                    obj.setValue(value)
            elif isinstance(obj, QtWidgets.QRadioButton):
                if settings.value("Gui/" + name) is not None:
                    value = settings.value("Gui/" + name)
                    if value is not None:
                        obj.setChecked(strtobool(value))
            elif isinstance(obj, QtWidgets.QCheckBox):
                if settings.value("Gui/" + name) is not None:
                    value = settings.value("Gui/" + name)
                    if value is not None:
                        obj.setChecked(strtobool(value))
            elif isinstance(obj, QtWidgets.QPushButton):
                if settings.value("Gui/" + name) is not None:
                    value = settings.value("Gui/" + name)
                    if value is not None:
                        obj.setChecked(strtobool(value))
            elif isinstance(obj, QtWidgets.QComboBox):
                if settings.value("Gui/" + name) is not None:
                    value = settings.value("Gui/" + name)
                    obj.setCurrentText(value)
            elif isinstance(obj, DoubleSlider):
                if settings.value("Gui/" + name) is not None:
                    value = float(settings.value("Gui/" + name))
                    obj.setValue(value)
