import sys, os, datetime
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QVBoxLayout,
    QLabel, QCheckBox, QComboBox, QLineEdit, QStyle,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QFrame, QPushButton
)
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMetaType, QRect

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


class MainWindow(QMainWindow):
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

    def click_press(self):
        self.counter += 1
        self.label.setText(f"PRESSED: {self.counter}")


class AbstractAppUIWidget(QWidget):
    pass


class AppEventHandler(object):
    def __int__(self, *args, **kwargs):
        pass

    def on_click(self, *args):
        pass

    # def on_

###################################################################


class SavedError(object):
    def __init__(self, e: Exception, description="ERROR"):
        self.error = e
        self.description = description
        self.created_at = datetime.datetime.utcnow()

    def __str__(self):
        return f"[{self.description}] {self.created_at} - {str(self.error)}"

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


t = Test()
t.on_click()



app = QApplication(sys.argv)
w = MainWindow()
w.showFullScreen()
# w.show()
app.exec_()
