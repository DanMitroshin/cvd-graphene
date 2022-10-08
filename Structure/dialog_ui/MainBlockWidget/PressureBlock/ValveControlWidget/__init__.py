from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath, QColor, QPainter
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, \
    QVBoxLayout, QLineEdit, QHBoxLayout, QLabel

from Structure.dialog_ui.components.butterfly_button import ButterflyButton
from .styles import styles, button_style


class ValveControlWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QWidget(self)
        self.line.setStyleSheet(styles.line)
        self.line.setFixedWidth(self.width() - 180)
        # print("HEIGHT!!!", self.height() // 2) # 240 = h/2 ????
        self.line.move(180, 60)  # -self.height() // 2

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setObjectName("valve_control_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.button = ValveControlButton()
        # self.button.setObjectName("button_valve_control")
        # self.button.setStyleSheet(button_style)

        self.b = ButterflyButton()

        self.layout.addStretch(2)
        self.layout.addWidget(self.button, stretch=1, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.b, stretch=4, alignment=QtCore.Qt.AlignHCenter,)


class ValveControlButton(QPushButton):
    def __init__(self):
        super().__init__()
        # self.setStyleSheet(styles.button_container)
        # self.button = QPushButton(self)
        # self.button.setObjectName("button_valve_control")
        # self.button.setStyleSheet(button_style)
        # self.button = QPushButton(self)
        self.setObjectName("button_valve_control")
        self.setStyleSheet(button_style)

    def paintEvent1(self, event):
        try:
            qp = QPainter()
            # qp.begin(self.button)
            qp.begin(self)

            # a = randint(10, 100)
            # d = a * math.tan(math.radians(30))
            x, y = 0, 20

            pos_1 = QPointF(x, y)
            pos_2 = QPointF(90, y)

            pos_3 = QPointF(x, y)
            pos_4 = QPointF(90, y + 30)

            qp.setBrush(QColor(0, 0, 0))
            path = QPainterPath()
            path.moveTo(pos_1)
            path.lineTo(pos_2)

            path2 = QPainterPath()
            path2.moveTo(pos_4)
            path2.lineTo(pos_3)

            # qp.rotate(7)
            qp.drawPath(path)
            qp.drawPath(path2)


            qp.end()
        except Exception as e:
            print("Draw line error", e)
        # painter = QtGui.QPainter(self.button)
        # painter.setPen(QtCore.Qt.black)
        # painter.translate(20, 100)
        # painter.rotate(-90)
        # painter.drawText(0, 0, "hellos")
        # painter.end()
