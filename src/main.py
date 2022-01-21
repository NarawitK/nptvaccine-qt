import sys
import resources.icons
from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from components.dailyui import DailyFilterWidget
from components.groupfilterui import VaccineGroupingSummary
from components.finvac_ui import FinvacWidget
from qt_material import apply_stylesheet


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NPTDailyVaccineGenerator")
        self.__layout = QtWidgets.QVBoxLayout()
        self.construct_tabs()
        
        container = QtWidgets.QWidget()
        container.setLayout(self.__layout)
        self.setCentralWidget(container)
    
    def construct_tabs(self):
        self.tabs = QtWidgets.QTabWidget()
        self.__dailyfilter_obj = DailyFilterWidget()
        self.__secondtab = VaccineGroupingSummary()
        self.__thirdtab = FinvacWidget()
        self.tabs.addTab(self.__dailyfilter_obj, "NPT Daily Report")
        self.tabs.addTab(self.__secondtab, "รายงานแยกวัคซีน")
        self.tabs.addTab(self.__thirdtab, "Financial Vac Report")
        self.__layout.addWidget(self.tabs)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/assets/icon.ico"))
    app.setOrganizationName("Kamphaeng Saen Hospital")
    app.setOrganizationDomain(".org")
    window = MainWindow()
    window.resize(900,450)
    apply_stylesheet(app, theme='dark_amber.xml')
    window.show()
    sys.exit(app.exec_())