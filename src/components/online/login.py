import os
from dotenv import load_dotenv
from PySide2 import QtCore, QtWidgets
from helper.api.passwordhasher import hash_password
from modules.worker import ReturnableWorker
from datafetch.api.authenticate import JWTVerifier, PublicKeyManager

load_dotenv()


class LoginMOPH(QtWidgets.QWidget):
    def __init__(self, mainwindow_instance, token_manager):
        super().__init__()
        self.mainwindow_instance = mainwindow_instance
        self.__token_manager = token_manager
        self.__thread_start_message = 'Authenticating . . .'
        self.__thread_error_message = 'Error:'
        self.__thread_finished_message = 'Logged in as'
        self.render_component()
        
    def render_component(self):

        # Layouts
        mainlayout = QtWidgets.QVBoxLayout()
        formlayout = QtWidgets.QFormLayout()

        # Login Widgets
        self.username_field = QtWidgets.QLineEdit()
        self.password_field = QtWidgets.QLineEdit()
        self.password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.hoscode_field = QtWidgets.QLineEdit()
        self.hoscode_field.setText(os.getenv('DEFAULT_HOSCODE'))
        self.login_btn = QtWidgets.QPushButton("&Login")
        self.login_btn.setAutoDefault(True)
        # self.response_label = QtWidgets.QLabel("Response")
        # self.response_field = QtWidgets.QTextEdit()
        # self.response_field.setReadOnly(True)

        # Assign Form Layout Widgets
        formlayout.addRow(self.tr("&UserName"), self.username_field)
        formlayout.addRow(self.tr("&Password"), self.password_field)
        formlayout.addRow(self.tr("&Hospital Code"), self.hoscode_field)


        # Signal-Slot Connect
        self.login_btn.clicked.connect(self.__on_login_btn_clicked)
        self.username_field.returnPressed.connect(self.__on_login_field_return_pressed)
        self.password_field.returnPressed.connect(self.__on_login_btn_clicked)

        # Assign MainLayout Widgets
        mainlayout.addLayout(formlayout)
        mainlayout.addWidget(self.login_btn)
        # mainlayout.addWidget(self.response_label)
        # mainlayout.addWidget(self.response_field)

        self.setLayout(mainlayout)

    def __login_form_validation(self, username, password, hospital_code):
        if username != '' and password != '' and hospital_code != '':
            return 1
        elif username == '':
            return 'Username'
        elif password == '':
            return 'Password'
        elif hospital_code == '':
            return 'Hospital Code'

    @QtCore.Slot()
    def __on_login_btn_clicked(self):
        validation_result = self.__login_form_validation(self.username_field.text(), self.password_field.text(), self.hoscode_field.text())
        if validation_result == 1:
            self.mainwindow_instance.set_statusbar_message("")
            self.start_worker(self.username_field.text(), self.password_field.text(), self.hoscode_field.text())
        else:
            self.mainwindow_instance.set_statusbar_message("You didn't fill {} yet".format(validation_result))

    @QtCore.Slot()
    def __on_login_field_return_pressed(self):
        self.__set_focus_on_widget(self.password_field)

    def __set_focus_on_widget(self, widget):
        widget.setFocus()

    def start_worker(self, *args):
        worker = ReturnableWorker(self.authentication, self.__thread_start_message, self.__thread_finished_message, self.__thread_error_message, *args)
        worker.signals.started.connect(self.on_worker_start)
        worker.signals.finished.connect(self.on_worker_finished)
        worker.signals.error.connect(self.on_worker_error)
        self.mainwindow_instance.threadpool.start(worker)

    @QtCore.Slot(str)
    def on_worker_start(self, message):
        self.mainwindow_instance.set_statusbar_message(message)
        # self.response_field.setText(message)
        self.login_btn.setEnabled(False)

    @QtCore.Slot(str)
    def on_worker_error(self, message):
        self.mainwindow_instance.set_statusbar_message(message)
        # self.response_field.setText(message)
        self.login_btn.setEnabled(True)

    @QtCore.Slot(str)
    def on_worker_finished(self, message):
        self.mainwindow_instance.set_statusbar_message(message)
        # self.response_field.setText(message)
        self.login_btn.setEnabled(True)

    def authentication(self, username, plain_password, hoscode):
        try:
            hashed_pw = hash_password(plain_password)
            self.__token_manager.get_token_from_moph(username, hashed_pw, hoscode)
            result = JWTVerifier.decoded_jwt(self.__token_manager.token, PublicKeyManager.try_read_key_from_file())
            return result['client']['name']
        except Exception as e:
            raise
