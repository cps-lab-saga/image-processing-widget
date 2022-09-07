import csv
import io
import itertools
import json
from fractions import Fraction

import cv2 as cv
import numpy as np

from image_processing_widget.custom_components import SpinBoxSlider
from image_processing_widget.defs import QtCore, QtWidgets, QtGui
from image_processing_widget.funcs.cv_enums import enum_border_types
from image_processing_widget.process_plugin import ProcessPlugin


class Filter2D(ProcessPlugin):
    def __init__(self):
        super().__init__()

        self.x_control = SpinBoxSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.x_control.setSingleStep(1)
        self.x_control.setRange(1, 100)
        self.x_control.setValue(3)
        self.x_control.valueChanged.connect(self.change_n_cols)
        self.form_layout.addRow("Kernel Width:", self.x_control)

        self.y_control = SpinBoxSlider(decimals=0, orientation=QtCore.Qt.Horizontal)
        self.y_control.setSingleStep(1)
        self.y_control.setRange(1, 100)
        self.y_control.setValue(3)
        self.y_control.valueChanged.connect(self.change_n_rows)
        self.form_layout.addRow("Kernel Height:", self.y_control)

        self.kernel_table_widget = QtWidgets.QTableWidget(parent=self)
        self.kernel_table_widget.verticalHeader().setVisible(False)
        self.kernel_table_widget.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.kernel_table_widget.horizontalHeader().setVisible(False)
        self.kernel_table_widget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.kernel_table_widget.setColumnCount(3)
        self.kernel_table_widget.setRowCount(3)

        for i, j in itertools.product(range(3), range(3)):
            item = QtWidgets.QTableWidgetItem(str(0))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.kernel_table_widget.setItem(i, j, item)

        self.kernel_table_widget.cellChanged.connect(
            lambda _: self.settings_updated.emit()
        )
        self.form_layout.addRow("Kernel:", self.kernel_table_widget)

        self.border_type = QtWidgets.QComboBox(self)
        self.border_type.addItems(enum_border_types.keys())
        self.form_layout.addRow("Border Types:", self.border_type)

        self.border_type.currentTextChanged.connect(
            lambda _: self.settings_updated.emit()
        )

    def change_n_rows(self, new_n_rows):
        n_row = self.kernel_table_widget.rowCount()
        n_col = self.kernel_table_widget.columnCount()

        diff = int(new_n_rows) - n_row
        if diff > 0:
            for _ in range(diff):
                self.kernel_table_widget.insertRow(n_row)
                for j in range(n_col):
                    item = QtWidgets.QTableWidgetItem(str(0))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.kernel_table_widget.setItem(n_row, j, item)
        elif diff < 0:
            for _ in range(abs(diff)):
                self.kernel_table_widget.removeRow(int(new_n_rows))

    def change_n_cols(self, new_n_cols):
        n_row = self.kernel_table_widget.rowCount()
        n_col = self.kernel_table_widget.columnCount()

        diff = int(new_n_cols) - n_col
        if diff > 0:
            for _ in range(diff):
                self.kernel_table_widget.insertColumn(n_col)
                for i in range(n_row):
                    item = QtWidgets.QTableWidgetItem(str(0))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.kernel_table_widget.setItem(i, n_col, item)
        elif diff < 0:
            for _ in range(abs(diff)):
                self.kernel_table_widget.removeColumn(int(new_n_cols))

    def paste_selection(self):
        if not (selection := self.kernel_table_widget.selectedIndexes()):
            return
        row_selected = sorted(index.row() for index in selection)[0]
        col_selected = sorted(index.column() for index in selection)[0]

        text = QtWidgets.QApplication.instance().clipboard().text()
        try:
            data = [list(row.split("\t")) for row in filter(None, text.split("\n"))]

            n_row = min(
                self.kernel_table_widget.rowCount() - row_selected,
                len(data),
            )
            n_col = min(
                self.kernel_table_widget.columnCount() - col_selected,
                len(data[0]),
            )
            for i, j in itertools.product(range(n_row), range(n_col)):
                item = self.kernel_table_widget.item(row_selected + i, col_selected + j)
                item.setText(str(data[i][j]))

        except Exception:
            return

    def copy_selection(self):
        if not (selection := self.kernel_table_widget.selectedIndexes()):
            return

        rows = sorted(index.row() for index in selection)
        columns = sorted(index.column() for index in selection)
        row_count = rows[-1] - rows[0] + 1
        col_count = columns[-1] - columns[0] + 1
        table = [[""] * col_count for _ in range(row_count)]
        for index in selection:
            row = index.row() - rows[0]
            column = index.column() - columns[0]
            table[row][column] = index.data()
        stream = io.StringIO()
        csv.writer(stream, dialect=csv.excel_tab).writerows(table)
        QtWidgets.QApplication.instance().clipboard().setText(stream.getvalue())

    def get_kernel(self):
        n_row = self.kernel_table_widget.rowCount()
        n_col = self.kernel_table_widget.columnCount()
        m = np.zeros((n_row, n_col))
        for i, j in itertools.product(range(n_row), range(n_col)):
            item = self.kernel_table_widget.item(i, j)
            if item is not None:
                try:
                    m[i, j] = float(item.text())
                except Exception:
                    m[i, j] = float(Fraction(item.text()))
        if (m - m.astype(int) == 0).all():
            m = m.astype(int)
        return m

    def set_kernel(self, m):
        n_row = self.kernel_table_widget.rowCount()
        n_col = self.kernel_table_widget.columnCount()
        for i, j in itertools.product(range(n_row), range(n_col)):
            item = self.kernel_table_widget.item(i, j)
            item.setText(str(m[i][j]))

    def process_img(self, img):
        border = enum_border_types[self.border_type.currentText()]
        kernel = self.get_kernel()
        return cv.filter2D(src=img, ddepth=-1, kernel=kernel, borderType=border)

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy):
            self.copy_selection()
        elif event.matches(QtGui.QKeySequence.Paste):
            self.paste_selection()
        event.accept()

    def gui_save(self, settings):
        super().gui_save(settings)
        settings.setValue(
            f"{self.save_heading}/kernal", json.dumps(self.get_kernel().tolist())
        )

    def gui_restore(self, settings):
        super().gui_restore(settings)
        if value := settings.value(f"{self.save_heading}/kernal"):
            self.set_kernel(json.loads(value))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Filter2D()
    widget.show()

    app.exec()
