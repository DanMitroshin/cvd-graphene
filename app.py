import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QVBoxLayout,
    QLabel, QCheckBox, QComboBox, QLineEdit, QStyle,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QFrame, QPushButton
)
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QMetaType, QRect

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

app = QApplication(sys.argv)
w = MainWindow()
w.showFullScreen()
# w.show()
app.exec()
