from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout
from .styles import styles


class RightButtonsWidget(QWidget):
    def __init__(self, on_close=None):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet("background-color: rgb(0, 0, 255);")

        self.button_close = QPushButton("CLOSE X")
        self.button_close.clicked.connect(on_close)
        self.button_close.setStyleSheet(styles.close_button)

        self.button_settings = QPushButton("SETTINGS")
        self.button_settings.setStyleSheet(styles.settings_button)

        self.select_recipe = QPushButton("Select and\nrun recipe")
        self.select_recipe.setStyleSheet(styles.run_recipe_button)

        self.edit_recipe = QPushButton("Edit\nrecipe")
        self.edit_recipe.setStyleSheet(styles.edit_recipe_button)

        self.layout.addWidget(self.button_close, 0, 0)
        # self.right_buttons_layout.setRowMinimumHeight(0, 10)
        # self.right_buttons_layout.setRowStretch(0, 10)

        self.layout.addWidget(self.button_settings, 1, 0)
        self.layout.setRowMinimumHeight(1, 370)
        # self.right_buttons_layout.setRowStretch(1, 1)

        self.layout.addWidget(self.select_recipe, 2, 0)
        self.layout.addWidget(self.edit_recipe, 3, 0)
