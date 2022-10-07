import sys, os, datetime
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QVBoxLayout,
    QLabel, QCheckBox, QComboBox, QLineEdit, QStyle,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QFrame, QPushButton
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QMetaType, QRect

from Core.exceptions.communicators import InactiveCommunicatorException
from Core.ui import StyleSheet
from Structure.dialog_ui import UiMainWindow, MainWindow

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

# s = StyleSheet({
#     "close_button": {
#         "height": "70px",
#         "font-size": "20px",
#         "background-color": "rgb(255, 150, 150)",
#     }
# })
# print("SSSSSSSSS", s.close_button)
# print("SSSSSSSSS 2", s.close_button1)
# sys.exit()

class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # line_style = QStyle()
        # line_style.sty

        line = QFrame()
        # line.setObjectName(QMetaType.Type.QString)
        line.setObjectName("ll")
        line.setLineWidth(100)
        line.setFixedHeight(100)
        line.setStyleSheet("background-color: rgb(255, 0, 50);")
        # line.setGeometry(QRect(0, 10, 100, 110))
        # line.setStyle()
        # line.setFrameShape(QFrame.Shape.HLine)
        # line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line = line

        self.line = QFrame()
        self.line.setMinimumWidth(100)
        self.line.setFixedHeight(20)
        # self.line.setGeometry(QRect(60, 110, 751, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                QtWidgets.QSizePolicy.Policy.Minimum)

        self.label = QLabel()
        # self.label.setStyleSheet('color:"red";font-size: 32;')
        self.label.setStyleSheet("""
        QWidget {
            border: 2px solid black;
            border-radius: 10px;
            background-color: rgb(255, 255, 255);
            font-size: 32px;
            max-width: 300px;
            }
        """)

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QHBoxLayout()
        layout_v = QVBoxLayout()
        layout.addWidget(self.line)
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        self.button_close = QPushButton("нажать для закрытия программы")
        self.button_close.clicked.connect(self.close)
        self.button_close.setStyleSheet("""
        QPushButton {
            height: 200px;
            font-size: 20px;
        }
        """)
        layout_v.addLayout(layout)
        self.button = QPushButton("Press Me!")
        self.button.setStyleSheet("""
                QPushButton {
                    height: 100px;
                    font-size: 16px;
                }
                """)
        self.counter = 0
        self.button.clicked.connect(self.click_press)

        layout_v.addWidget(self.button)
        layout_v.addWidget(self.button_close)

        container = QWidget()
        container.setLayout(layout_v)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

    def click_press(self):
        self.counter += 1
        self.label.setText(f"PRESSED: {self.counter}")

    def show_time(self):
        print("TIME:", datetime.datetime.now())

class AbstractAppUIWidget(QWidget):
    pass



###################################################################


class Test:

    def handler_decorator(func):
        def magic(self):
            print("start magic")
            self.check()
            func(self)
            print("end magic")

        return magic

    def __init__(self):
        self.counter = 123
        print("COUNTER SET UP!")

    @handler_decorator
    def on_click(self):
        print("ON CLICK, Counter:", self.counter)

    def check(self):
        self.counter += 1
        print("CHECK COUNTER:", self.counter)


# t = Test()
# t.on_click()

# def bar():
#     raise InactiveCommunicatorException(communicator_id="ref_234")
#
# bar()

# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = UiMainWindow()
# ui.setup_ui(MainWindow)
# MainWindow.showFullScreen()
# sys.exit(app.exec_())


app = QApplication([])
w = MainWindow()
# w.show()
w.showFullScreen()
w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
# w.setWindowFlags(Qt.WindowType_Mask)
app.exec()
