from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, \
    QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, QHBoxLayout

from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .styles import styles, button_on_style, button_off_style


class FlowControlWidget(QWidget):
    def __init__(self, title="Title"):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.title = QLabel()
        self.title.setText(title)
        self.title.setStyleSheet(styles.title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.buttons = QHBoxLayout()
        self.button_on = QPushButton()
        self.button_on.setObjectName("button_on_flow")
        self.button_on.setStyleSheet(button_on_style)
        self.button_off = QPushButton()
        self.button_off.setStyleSheet(button_off_style)

        self.buttons.addWidget(self.button_on)
        self.buttons.addWidget(self.button_off)
        self.layout.addLayout(self.buttons)
