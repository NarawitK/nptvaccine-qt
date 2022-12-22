from typing import Callable
from PySide2 import QtWidgets


class SaveButtonComponent(QtWidgets.QWidget):
    def __init__(self, save_button_label: str = "Save", clear_button_label: str = "None"):
        super().__init__()
        self.__main_layout = None
        self.save_btn = None
        self.__save_func: Callable = None
        self.clear_btn = None
        self.__clear_func: Callable = None
        self.__render_components(save_button_label, clear_button_label)

    def __render_components(self, save_button_label: str = "Save", clear_button_label: str = "None"):
        self.__main_layout = QtWidgets.QHBoxLayout(self)
        self.save_btn = QtWidgets.QPushButton(save_button_label)
        self.save_btn.clicked.connect(self.__on_save_button_clicked)
        self.__main_layout.addWidget(self.save_btn)
        if clear_button_label != "None":
            self.clear_btn = QtWidgets.QPushButton(clear_button_label)
            self.clear_btn.clicked.connect(self.__on_clear_button_clicked)
            self.__main_layout.addWidget(self.clear_btn)

    def __on_save_button_clicked(self):
        if self.__save_func is not None:
            self.__save_func()
        else:
            raise NotImplementedError("Save function not yet implemented")

    def __on_clear_button_clicked(self):
        if self.clear_btn is not None and self.__clear_func is not None:
            self.__clear_func()
        else:
            raise NotImplementedError("Save function not yet implemented")

    def set_save_func(self, func: Callable):
        self.__save_func = func

    def set_clear_func(self, func: Callable):
        if self.clear_btn is not None:
            self.__clear_func = func
        else:
            raise NotImplementedError("Clear Button is not implemented")
