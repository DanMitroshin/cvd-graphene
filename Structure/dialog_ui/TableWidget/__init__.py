import os
import string
from random import choice

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QFileDialog,\
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QHeaderView
from PyQt5.QtCore import QSize, Qt

from Core.actions import ACTIONS, get_action_by_name, AppAction
from Core.settings import TABLE_COLUMN_NAMES
from .styles import styles


def random_str(length=5):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(choice(letters) for _ in range(length))


def create_recipe_file_name():
    return "recipe_" + random_str()


class TableItem(object):
    def __init__(self, widget):
        self.widget = widget
        # if isinstance(self.widget, QTableWidgetItem):
        #     w = QTableWidgetItem()
        #     w.s
        #     widget.

    @property
    def is_item(self):
        if isinstance(self.widget, QTableWidgetItem):
            return True
        return False


class TableRow(object):

    def __init__(self, table, row_id, items=None):
        self.table = table
        self.row_id = row_id
        self.items = None

        self.combo = QComboBox()
        # self.combo.te
        self.combo.addItems(list(map(lambda x: x.name, ACTIONS)))

        try:
            self.combo.setCurrentIndex(0)
        except Exception as e:
            print("Ind err:", e)

        # print("INDEX:", self.combo.currentIndex())

        if items is not None and len(items) >= 5:
            items = list(map(lambda x: str(x).strip(), items))
            action, i = get_action_by_name(name=items[0])
            action: AppAction = action
            if action is not None:
                self.combo.setCurrentIndex(i)
                self.items = [TableItem(self.combo)] + [
                    TableItem(QTableWidgetItem(s)) for s in items[1:]
                ]
                if len(action.args_info) >= 1 and action.args_info[0].arg_type == list:
                    combo2 = QComboBox()
                    combo2.addItems(action.args_info[0].arg_list)
                    combo2.setCurrentIndex(min(0, action.args_info[0].arg_list.index(items[1])))
                    self.items[1] = TableItem(combo2)

        if self.items is None:
            self._set_default_table_items()

        self.combo.currentIndexChanged.connect(self._action_changed)

    def _set_default_table_items(self):
        self.items = [
            TableItem(self.combo),
            TableItem(QTableWidgetItem('')),
            TableItem(QTableWidgetItem('')),
            TableItem(QTableWidgetItem('')),
            TableItem(QTableWidgetItem('')),
        ]

    def __iter__(self):
        self._ind = 0
        return self

    def __next__(self):
        if self._ind < len(self.items):
            x = self.items[self._ind]
            self._ind += 1
            return x
        else:
            raise StopIteration

    def _table_update(self):
        self.table.update_row(self.row_id, self.items)

    def _action_changed(self):
        self._set_default_table_items()
        index = self.combo.currentIndex()
        # print("Update index:", index)
        action = ACTIONS[index]
        for j, arg in enumerate(action.args_info):
            if arg.arg_type == list:
                combo2 = QComboBox()
                combo2.addItems(arg.arg_list)
                combo2.setCurrentIndex(0)
                self.items[j + 1] = TableItem(combo2)
            elif arg.arg_default is not None:
                self.items[j + 1] = TableItem(QTableWidgetItem(str(arg.arg_default)))

        self._table_update()


class AppTableWidget(QWidget):

    def __init__(self, parent=None, save_recipe_file=None, get_recipe_file_data=None):
        # You must call the super class method
        super().__init__(parent)

        self.save_recipe_file = save_recipe_file
        self.get_recipe_file_data = get_recipe_file_data

        self.file = None
        self.path = None

        self.file_path = None  # for directly open files

        self.setObjectName("AppTableWidget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # central_widget = QWidget(self)  # Create a central widget
        # self.setCentralWidget(central_widget)  # Install the central widget

        grid_layout = QGridLayout()  # Create QGridLayout
        self.setLayout(grid_layout)
        # QApplication.desktop().width(),
        # QApplication.desktop().height()
        self.setMinimumSize(QSize(
            QApplication.desktop().width() * 0.99,
            QApplication.desktop().height() * 0.99
        ))  # Set sizes
        self.row_count = 1
        self.rows = [TableRow(table=self, row_id=0)]

        table = QTableWidget()  # Create a table
        table.setColumnCount(5)  # Set three columns
        table.setRowCount(self.row_count)  # and one row

        # Set the table headers
        table.setHorizontalHeaderLabels(TABLE_COLUMN_NAMES)

        # self.combo = QComboBox()
        # self.combo.te
        # self.combo.addItems(["option1", "option2", "option3", "option4"])
        # self.comboBox.currentIndexChanged.connect(slotLambda)

        # Set the tooltips to headings
        table.horizontalHeaderItem(0).setToolTip("Процесс")
        table.horizontalHeaderItem(1).setToolTip("Аргумент")
        table.horizontalHeaderItem(2).setToolTip("Аргумент")
        table.horizontalHeaderItem(3).setToolTip("Аргумент")
        table.horizontalHeaderItem(4).setToolTip("Комментарий")

        # Set the alignment to the headers
        # table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        # # table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        # table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignRight)

        self.table = table

        add_row_button = QPushButton('+ добавить строку')
        add_row_button.clicked.connect(self._add_row)
        add_row_button.setObjectName("table_button")
        add_row_button.setStyleSheet(styles.table_button)

        # get_values_button = QPushButton('print values')
        # get_values_button.clicked.connect(self._get_values)
        buttons_layout = QHBoxLayout()

        save_button = QPushButton("SAVE RECIPE")
        save_button.clicked.connect(self.save_recipe)
        save_button.setObjectName("table_button")
        save_button.setStyleSheet(styles.table_button)

        close_button = QPushButton("CLOSE")
        close_button.clicked.connect(self.on_close)
        close_button.setObjectName("table_button")
        close_button.setStyleSheet(styles.table_button)

        name = QLineEdit()
        name.setPlaceholderText("Название файла...")
        name.setText(create_recipe_file_name())
        self.file_name_widget = name
        self.file_name_widget.setObjectName("table_name_input")
        self.file_name_widget.setStyleSheet(styles.table_name_input)

        buttons_layout.addWidget(self.file_name_widget)
        buttons_layout.addWidget(save_button)
        # buttons_layout.addWidget(get_values_button)
        buttons_layout.addWidget(close_button)

        grid_layout.addLayout(buttons_layout, 0, 0)
        grid_layout.addWidget(table, 1, 0)  # Adding the table to the grid
        grid_layout.addWidget(add_row_button, 2, 0)
        # grid_layout.addWidget(get_values_button, 1, 1)

        self._update_table()
        self.hide()

    def _update_table_ui(self):
        horizontalHeader = self.table.horizontalHeader()
        # resize the first column to 100 pixels
        for i in range(4):
            horizontalHeader.resizeSection(i, 180)
        # adjust the second column to its contents
        # horizontalHeader.setSectionResizeMode(
        #     1, QHeaderView.ResizeToContents)
        # adapt the third column to fill all available space
        # horizontalHeader.setSectionResizeMode(
        #     4, QHeaderView.Stretch)
        # Do the resize of the columns by content
        self.table.resizeColumnsToContents()
        horizontalHeader.setSectionResizeMode(
            4, QHeaderView.Stretch)

    def on_create_recipe(self):
        self.show()
        print("On create recipe show!!!")

    def on_open_recipe_file(self, file_path, data):
        try:
            self.file_path = file_path
            self.row_count = len(data)
            self.table.setRowCount(self.row_count)
            self.rows = []
            for i, row in enumerate(data):
                table_row = TableRow(table=self, row_id=i, items=row)
                self.rows.append(table_row)
            self._update_table()
            # self.rows = [TableRow(table=self, row_id=0)]
            file_name = os.path.basename(file_path)
            self.file_name_widget.setText(file_name)
            self.file_name_widget.setEnabled(False)
            self.show()
        except Exception as e:
            print("Open recipe file error UI:", e)

    def set_target_file(self, path=None, file=None):
        self.file = file
        self.path = path

    def update_row(self, row_id, items):
        for i, item in enumerate(items):
            if item.is_item:
                try:
                    self.table.removeCellWidget(row_id, i)
                    # self.table.cellW
                except:
                    pass
                self.table.setItem(row_id, i, item.widget)
            else:
                self.table.setCellWidget(row_id, i, item.widget)
            # table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
            # table.setItem(0, 2, QTableWidgetItem("Text in column 3"))
            # self.table.resizeColumnsToContents()

    def _update_table(self):
        for i, row in enumerate(self.rows):
            self.update_row(i, row)
        self._update_table_ui()
        # self.table.resizeColumnsToContents()

    def _add_row(self):
        self.row_count += 1
        self.table.setRowCount(self.row_count)  # and one row
        self.rows.append(TableRow(table=self, row_id=self.row_count - 1))
        self._update_table()

    def _get_values(self):
        try:
            arr = []
            for row in range(self.table.rowCount()):
                row_arr = []
                for col in range(self.table.columnCount()):
                    it = self.table.item(row, col)
                    it2 = self.table.cellWidget(row, col)
                    if it2 is not None:
                        row_arr.append(it2.currentText())
                        continue
                    if it is None:
                        row_arr.append('')
                        continue

                    if hasattr(it, 'text'):
                        row_arr.append(it.text())
                    elif hasattr(it, 'currentText'):
                        row_arr.append(it.currentText())
                arr.append(row_arr)
            print("TABLE:", arr)
            return arr

        except Exception as e:
            print("Err get value table:", e)

    def save_recipe(self):
        try:
            has_file_path = bool(self.file_path)

            if not self.path and not has_file_path:
                path = QFileDialog.getExistingDirectory(self, "Выберите папку", "")
                if path:
                    self.path = path
                else:
                    return
            file_name = self.file_name_widget.text()
            if file_name.endswith('.xlsx'):
                self.file = file_name
            else:
                self.file = file_name + '.xlsx'

            arr = self._get_values()
            self.save_recipe_file(
                file=self.file,
                path=self.path,
                file_path=self.file_path,
                data=arr
            )
        except Exception as e:
            print("Save file error:", e)

    def on_close(self):
        self.file = None
        self.path = None
        self.file_path = None
        self.file_name_widget.setText(create_recipe_file_name())
        self.file_name_widget.setEnabled(True)
        self.hide()

        self.row_count = 1
        self.rows = [TableRow(table=self, row_id=0, items=None)]
        self.table.setRowCount(self.row_count)  # and one row
        self._update_table()