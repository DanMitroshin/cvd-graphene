from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout

from .SetTemperatureBlock import SetTemperatureBlock
from .styles import styles


class TemperatureBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.set_temperature = SetTemperatureBlock()
        self.layout.addWidget(self.set_temperature, QtCore.Qt.AlignTop)
