from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QHBoxLayout

from .PressureBlock import PressureBlock
from .PressureControlBlock import PressureControlBlock
from .TemperatureBlock import TemperatureBlock
from .styles import styles


class MainBlockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("main_block_widget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet("* {background-color: rgb(0, 0, 255);}")

        self.pressure_block = PressureBlock()
        self.layout.addWidget(self.pressure_block)

        self.pressure_control_block = PressureControlBlock()
        self.layout.addWidget(self.pressure_control_block)

        self.temperature_block = TemperatureBlock()
        self.layout.addWidget(self.temperature_block)
