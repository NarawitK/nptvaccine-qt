import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QWidget,\
    QVBoxLayout,\
    QHBoxLayout,\
    QLabel, \
    QListWidget, \
    QLineEdit, \
    QPushButton, QAbstractItemView
from typing import Callable
from helper.helper import swap_position


class ListEditorComponent(QWidget):
    DEFAULT_ADD_BTN_LABEL = "Add"
    DEFAULT_EDIT_BTN_LABEL = "Edit"
    DEFAULT_REMOVE_BTN_LABEL = "Remove"
    UNBOUND_LISTBOX_INDEX = -1
    onAddItem = QtCore.Signal(str)
    onEditItem = QtCore.Signal(str, str, int)
    onRemoveItem = QtCore.Signal(str)

    def __init__(self, label: str, data_list: list = [], btn_labels: list = [DEFAULT_ADD_BTN_LABEL, DEFAULT_EDIT_BTN_LABEL, DEFAULT_REMOVE_BTN_LABEL], is_dragable_list: bool = True):
        super().__init__()
        self.__data_list = []
        if type(data_list) is dict:
            for key in data_list:
                self.__data_list.append(key)
        elif type(data_list) is list:
            self.__data_list = data_list
        else:
            raise ValueError("Value Type not Support")
        self.line_edit = None
        self.listbox = None
        self.label = None
        self.__main_layout = None
        self.__sub_layout = None
        self.__init_component(label, btn_labels, is_dragable_list)

    def __init_component(self, label: str, btn_labels: list, is_dragable_list: bool = True):
        self.__main_layout = QVBoxLayout(self)
        self.__sub_layout = QHBoxLayout()
        self.__button_layout = QVBoxLayout()
        self.__button_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QLabel(label)
        self.listbox = QListWidget()
        
        self.listbox.addItems(self.__data_list)
        self.line_edit = QLineEdit()

        # Add, Remove Button Declaration Here
        self.__add_button = QPushButton(btn_labels[0])
        self.__edit_button = QPushButton(btn_labels[1])
        self.__remove_button = QPushButton(btn_labels[2])
        self.__edit_button.setEnabled(False)
        self.__remove_button.setEnabled(False)
        
        # Add Buttons to sub_layout
        self.__button_layout.addWidget(self.__add_button)
        self.__button_layout.addWidget(self.__edit_button)
        self.__button_layout.addWidget(self.__remove_button)

        # Add Normally Widget
        self.__main_layout.addWidget(self.label)
        self.__sub_layout.addWidget(self.listbox)

        # Composing Layout Inner -> Outer
        self.__sub_layout.addLayout(self.__button_layout)
        self.__main_layout.addLayout(self.__sub_layout)
        self.__main_layout.addWidget(self.line_edit)

        # Dragable Condition
        if is_dragable_list:
            self.listbox.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
            self.listbox.model().rowsMoved.connect(self.__on_rows_moved)

        # Wiring Signal to Slot
        self.listbox.currentItemChanged.connect(self.__on_current_item_changed)
        self.__add_button.clicked.connect(self.__on_add_btn_click)
        self.__edit_button.clicked.connect(self.__on_edit_button_clicked)
        self.__remove_button.clicked.connect(self.__on_remove_btn_click)

    def get_data_list(self) -> list:
        return self.__data_list

    def set_data_list(self, data_list: list = []):
        self.__data_list = data_list
        self.listbox.clear()
        self.listbox.addItems(data_list)

    # Slots
    def __on_current_item_changed(self, current_item):
        if current_item is not None:
            self.line_edit.setText(current_item.text())
            self.__edit_button.setEnabled(True)
            self.__remove_button.setEnabled(True)
        else:
            self.__edit_button.setEnabled(False)
            self.__remove_button.setEnabled(False)

    def __on_rows_moved(self, _, source_start_index, source_end_index, __, destination_index):
        self.__data_list = swap_position(self.__data_list, source_start_index, destination_index)
        print(self.__data_list)

    def __on_add_btn_click(self):
        text_from_line_edit: str = self.line_edit.text()
        if text_from_line_edit is not None and text_from_line_edit != "":
            self.listbox.addItem(text_from_line_edit)
            self.listbox.scrollToBottom()
            self.__data_list.append(text_from_line_edit)
            self.onAddItem.emit(text_from_line_edit)

    def __on_edit_button_clicked(self):
        current_index = self.listbox.currentRow()
        if current_index > self.UNBOUND_LISTBOX_INDEX:
            cur_item = self.listbox.currentItem()
            text_from_line_edit: str = self.line_edit.text()
            if text_from_line_edit is not None and text_from_line_edit != "":
                self.__data_list[current_index] = text_from_line_edit
                self.onEditItem.emit(text_from_line_edit, cur_item.text(), current_index)
                cur_item.setText(text_from_line_edit)

    def __on_remove_btn_click(self):
        self.__edit_button.setEnabled(False)
        current_index = self.listbox.currentRow()
        if current_index > self.UNBOUND_LISTBOX_INDEX:
            del self.__data_list[current_index]
            remove_value = self.listbox.takeItem(current_index)
            self.onRemoveItem.emit(remove_value.text())

    def set_on_add_button_slot(self, func: Callable):
        self.__add_button.clicked.connect(func)

    def set_on_edit_button_slot(self, func: Callable):
        self.__edit_button.clicked.connect(func)

    def set_on_remove_button_slot(self, func: Callable):
        self.__remove_button.clicked.connect(func)

    def set_on_current_item_changed_slot(self, func: Callable):
        self.listbox.currentItemChanged.connect(func)
