import re
from PySide2 import QtWidgets, QtCore


class NPTSettingComponent(QtWidgets.QWidget):
    LABEL = "ลิ้งค์เชื่อมต่อไปที่ Google Sheet ของ NPTVaccine"
    STATE_LABEL_TEXT = "Not a valid URL"
    STATE_TEXT_STYLESHEET = "color: red"
    URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    onUrlValid = QtCore.Signal(str)

    def __init__(self, url: str = ""):
        super().__init__()
        self.__is_url_valid: bool = False
        self.__main_layout = None
        self.__npt_url_editor_label = None
        self.__npt_url_editor: QtWidgets.QLineEdit = None
        self.__state_text = None
        self.__render_components(url)

    def __render_components(self, url: str = ""):
        self.__main_layout = QtWidgets.QVBoxLayout(self)
        self.__state_text = QtWidgets.QLabel()
        self.__state_text.setVisible(True)
        self.__state_text.setText(self.STATE_LABEL_TEXT)
        self.__state_text.setStyleSheet(self.STATE_TEXT_STYLESHEET)
        self.__npt_url_editor_label = QtWidgets.QLabel(self.LABEL)
        self.__npt_url_editor = QtWidgets.QLineEdit()
        self.__npt_url_editor.textChanged.connect(self.__on_editor_text_changed)
        self.__npt_url_editor.setText(url)
        # Set Layout
        self.__main_layout.addWidget(self.__npt_url_editor_label)
        self.__main_layout.addWidget(self.__npt_url_editor)
        self.__main_layout.addWidget(self.__state_text)

    def get_editor_text(self):
        if self.__is_url_valid:
            return self.__npt_url_editor.text()

    def set_editor_text(self, text: str):
        self.__npt_url_editor.setText(text)

    def __on_editor_text_changed(self, text: str):
        if re.match(self.URL_REGEX, text) is not None:
            self.__is_url_valid = True
            self.__state_text.setVisible(not self.__is_url_valid)
            self.onUrlValid.emit(text)
        else:
            self.__is_url_valid = False
            self.__state_text.setVisible(not self.__is_url_valid)
