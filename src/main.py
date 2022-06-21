import sys
import resources.icons
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
from qt_material import apply_stylesheet
from components.dailyui import DailyFilterWidget
from components.groupfilterui import VaccineGroupingSummary
from components.finvac_ui import FinvacWidget
from components.weeklyui import WeeklyFilterWidget
from components.online.login import LoginMOPH
from components.online.crosscheckui import CrossCheckComponent
from datafetch.api.authenticate import AuthenticateTokenManager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusbar = self.statusBar()
        self.threadpool = QtCore.QThreadPool()
        self.setWindowTitle("NPTDailyVaccineGenerator")
        self.token_manager = AuthenticateTokenManager()
        layout = QtWidgets.QVBoxLayout()
        
        # TO-DO: Using Qt StatusBar and token_man
        self.__innertab = InnerTab(self)
        self.__outertab = OuterTab(self)

        self.__construct_tabs(layout)
        
        main_container = QtWidgets.QWidget()
        main_container.setLayout(layout)
        self.setCentralWidget(main_container)
    
    def __construct_tabs(self, layout):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.__innertab, "Offline Features")
        tabs.addTab(self.__outertab, "Online Features")
        layout.addWidget(tabs)

    def set_statusbar_message(self, message):
        self.statusbar.showMessage(message)


class OuterTab(QtWidgets.QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.__layout = QtWidgets.QVBoxLayout()
        self.__construct_tabs(mainwindow)
    
    def __construct_tabs(self, mainwindow):
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(LoginMOPH(mainwindow, mainwindow.token_manager), "Login MOPH-IC")
        self.tabs.addTab(CrossCheckComponent(mainwindow, mainwindow.token_manager), "X Check")
        self.__layout.addWidget(self.tabs)
        self.setLayout(self.__layout)


class InnerTab(QtWidgets.QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.__layout = QtWidgets.QVBoxLayout()
        self.__construct_tabs(mainwindow)
    
    def __construct_tabs(self, mainwindow):
        self.tabs = QtWidgets.QTabWidget()
        self.__dailyfilter_screen = DailyFilterWidget()
        self.__vac_group_screen = VaccineGroupingSummary()
        self.__fin_vac_screen = FinvacWidget()
        self.__weekly_group_screen = WeeklyFilterWidget()
        self.tabs.addTab(self.__dailyfilter_screen, "NPT Daily Report")
        self.tabs.addTab(self.__vac_group_screen, "Separate Vaccine Report")
        self.tabs.addTab(self.__fin_vac_screen, "Financial Vac Report")
        self.tabs.addTab(self.__weekly_group_screen, "Weekly Group Report")
        self.__layout.addWidget(self.tabs)
        self.setLayout(self.__layout)

'''
#For Clean-up authenticator and remove some file(s)
def onAppExit(app):
    app_exec_stat = app.exec_()
    sys.exit(app_exec_stat)
'''

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/assets/icon.ico"))
    app.setOrganizationName("KamphaengSaen Hospital")
    app.setOrganizationDomain(".org")
    window = MainWindow()
    window.resize(800, 600)
    apply_stylesheet(app, theme='dark_amber.xml')
    window.show()
    sys.exit(app.exec_())
    # onAppExit(app)
