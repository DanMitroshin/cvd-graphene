import pandas as pd
from math import isnan
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QFileDialog,\
    QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import QSize, Qt

from Core.settings import RRG_LIST, GAS_LIST

COLUMNS = ["Процесс", "Аргумент 1", "Аргумент 2", "Аргумент 3", "Комментарий"]


def safe_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Check error: {str(e)}"
    return wrapper


class Argument:
    arg_type = None
    arg_default = None
    arg_list = None

    @safe_check
    def check(self, value):
        pass


class FloatArgument(Argument):
    arg_type = float
    arg_default = 0.0

    @safe_check
    def check(self, value):
        value = float(value)


class GasListArgument(Argument):
    arg_type = list
    arg_list = GAS_LIST

    @safe_check
    def check(self, value):
        value = str(value).strip()
        if value not in self.arg_list:
            raise Exception(f"Gas {value} not in gas list")


class RrgListArgument(Argument):
    arg_type = list
    arg_list = RRG_LIST

    @safe_check
    def check(self, value):
        value = str(value).strip()
        if value not in self.arg_list:
            raise Exception(f"Rrg {value} not in rrg list")


class AppAction:
    args_info = []
    args_amount = 0

    def __init__(self, name, args_amount=None):
        self.name = name
        if args_amount is not None:
            self.args_amount = args_amount

    def check_args(self):
        return None


class RrgSelectAction(AppAction):
    args_info = [GasListArgument]
    args_amount = 1


class OpenValveAction(RrgSelectAction):
    pass


class CloseValveAction(RrgSelectAction):
    pass


ACTIONS = [
    AppAction("Pause"),
    OpenValveAction("Open valve"),
    CloseValveAction("Close valve"),
    AppAction("Act 1", args_amount=2),
    AppAction("Act 2", args_amount=3),
    AppAction("Act 3", args_amount=1),
    AppAction("Act 4", args_amount=1),
    AppAction("Act ХХХ", args_amount=1),
]


def get_action_by_name(name):
    for i, action in enumerate(ACTIONS):
        if action.name == name:
            return action, i
    return None, 0


class TableItem(object):
    def __init__(self, widget):
        self.widget = widget

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

    def __init__(self, parent=None):
        # You must call the super class method
        super().__init__(parent)

        # central_widget = QWidget(self)  # Create a central widget
        # self.setCentralWidget(central_widget)  # Install the central widget

        grid_layout = QGridLayout()  # Create QGridLayout
        self.setLayout(grid_layout)
        # QApplication.desktop().width(),
        # QApplication.desktop().height()
        self.setMinimumSize(QSize(
            QApplication.desktop().width() * 0.9, QApplication.desktop().height() * 0.9))  # Set sizes
        self.row_count = 1
        self.rows = [TableRow(table=self, row_id=0)]

        table = QTableWidget()  # Create a table
        table.setColumnCount(5)  # Set three columns
        table.setRowCount(self.row_count)  # and one row

        # Set the table headers
        table.setHorizontalHeaderLabels(COLUMNS)

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
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        # table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignRight)

        # Fill the first line
        # table.setItem(0, 0, QTableWidgetItem("Text in column 1",))
        # table.setCellWidget(0, 0,  self.combo)
        # table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        # table.setItem(0, 2, QTableWidgetItem("Text in column 3"))
        self.table = table

        # Do the resize of the columns by content
        table.resizeColumnsToContents()

        add_row_button = QPushButton('+ добавить строку')
        add_row_button.clicked.connect(self._add_row)

        get_values_button = QPushButton('print values')
        get_values_button.clicked.connect(self._get_values)
        buttons_layout = QHBoxLayout()

        save_button = QPushButton("SAVE RECIPE")
        save_button.clicked.connect(self.save_recipe)

        close_button = QPushButton("CLOSE")
        close_button.clicked.connect(self.show_dialog)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(get_values_button)
        buttons_layout.addWidget(close_button)

        grid_layout.addLayout(buttons_layout, 0, 0)
        grid_layout.addWidget(table, 1, 0)  # Adding the table to the grid
        grid_layout.addWidget(add_row_button, 2, 0)
        # grid_layout.addWidget(get_values_button, 1, 1)

        self._update_table()

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
            self.table.resizeColumnsToContents()

    def _update_table(self):
        for i, row in enumerate(self.rows):
            self.update_row(i, row)
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
            arr = self._get_values()
            if arr is None:
                return
            df = pd.DataFrame(arr, columns=COLUMNS)
            # df.
            path = "recipes/test3.xlsx"
            df.to_excel(excel_writer=path)
            excel_data_df = pd.read_excel(path, header=None)
            # for a in excel_data_df:
            #     print("AA", a)
            cols = excel_data_df.columns.ravel()
            arr = []
            for col in cols[1:]:
                a = excel_data_df[col].tolist()[1:]
                for i in range(len(a)):
                    if isnan(a[i]):
                        a[i] = ""
                arr.append(a)
            print("M", arr)
        except Exception as e:
            print("Save err", e)

    def show_dialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '')[0]
        print("CHOOSE FILE:", fname)

        # f = open(fname, 'r')
        #
        # with f:
        #     data = f.read()
        #     self.textEdit.setText(data)

    def on_close(self):
        self.hide()
