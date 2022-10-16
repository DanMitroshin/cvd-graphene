from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect

from Structure.dialog_ui.components import ParameterLatexLabel, ParameterLabel
from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .ActualTemperature import ActualTemperature
from .RiseCurrentBlock import RiseCurrentBlock
from .SetCurrentBlock import SetCurrentBlock
from .styles import styles


class CurrentSettingsBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("current_settings_block")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.actual_temperature = ActualTemperature()
        self.layout.addWidget(self.actual_temperature, QtCore.Qt.AlignTop)

        self.set_current_block = SetCurrentBlock()
        self.layout.addWidget(self.set_current_block, )

        self.voltage_label = ParameterLabel()
        self.voltage_label.setText("U = 5,6347 V")

        self.layout.addWidget(self.voltage_label,
                              alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.rise_current_block = RiseCurrentBlock()
        self.layout.addWidget(self.rise_current_block, QtCore.Qt.AlignCenter)
