from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .styles import styles


class ShowPressureBlock(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setText("P = 1,3 * 10000 mbar")
        shadow = QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # adding shadow to the label
        self.setGraphicsEffect(shadow)
