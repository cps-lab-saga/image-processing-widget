import importlib.metadata
from time import sleep

from image_processing_widget.defs import QtCore, QtGui, QtWidgets, resource_dir


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, length=100):
        super().__init__()

        self.setFixedSize(600, 300)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.move(  # move to centre of screen
            QtWidgets.QApplication.primaryScreen().geometry().center()
            - self.rect().center()
        )

        self.version = importlib.metadata.version("image_processing_widget")

        self.frame = QtWidgets.QFrame(self)
        self.frame.setObjectName("Frame")
        self.frame.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.main_layout.addWidget(self.frame)
        self.frame_layout = QtWidgets.QVBoxLayout(self.frame)

        title_row = QtWidgets.QHBoxLayout(self.frame)
        self.frame_layout.addLayout(title_row)

        icon_size = 200
        self.icon_label = QtWidgets.QLabel(self.frame)
        self.icon_label.setPixmap(
            QtGui.QIcon(str(resource_dir() / "camera.svg")).pixmap(icon_size)
        )
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        title_row.addWidget(self.icon_label)

        self.title_label = QtWidgets.QLabel(self.frame)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setText("Image\nProcessing\nWidget")
        title_row.addWidget(self.title_label)

        self.subtitle_label = QtWidgets.QLabel(self.frame)
        self.subtitle_label.setObjectName("SubTitleLabel")
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle_label.setText(f"Fukuda-Yeoh Lab 2022\t v{self.version}")
        self.frame_layout.addWidget(self.subtitle_label)

        self.progress_bar = QtWidgets.QProgressBar(self.frame)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar.setMaximum(length)
        self.frame_layout.addWidget(self.progress_bar)

        self.frame.setStyleSheet(
            """
            #Frame {
                background-color: #efefef;
                border-radius: 20px;
                border-color: white;
            }
            """
        )
        self.title_label.setStyleSheet(
            'font-family: "Arial";'
            "font-weight: Bold;"
            "font-size: 32px;"
            "color: black;"
        )
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: gray;
                color: white;
                border-style: none;
                border-radius: 15px;
                font-family: "Arial";
                font-weight: Bold;
                font-size: 20px;
            }

            QProgressBar::chunk {
                border-radius: 15px;
                background: qlineargradient(
                    x1: 0, y1: 0.5, x2: 1, y2: 0.5, 
                    stop: 0 rgb(108, 171, 192),  stop: 1 rgb(28, 51, 78));
            }
            """
        )

    def set_progress(self, value):
        self.progress_bar.setValue(value)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    splash = SplashScreen()
    splash.show()

    for i in range(10):
        splash.set_progress(i * 10)
        app.processEvents()
        sleep(1)
