import sys
from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from components.subcomponents.mainmenu_tab_widget import MainMenuTabWidget
from qt_material import apply_stylesheet


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NPTDailyVaccineGenerator")
        self.__scroll_view = QtWidgets.QScrollArea()
        self.__main_widget = MainMenuTabWidget()
        self.__scroll_view.setWidget(self.__main_widget)
        self.__scroll_view.setWidgetResizable(True)
        self.setCentralWidget(self.__scroll_view)

    def calc_screen_size(self, width, height):
        w = width * 0.5
        h = height * 0.7
        return (w,h)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icon.ico"))
    app.setOrganizationName("Kamphaeng Saen Hospital")
    app.setOrganizationDomain(".org")
    window = MainWindow()
    size = app.primaryScreen().size()
    calculated_size = window.calc_screen_size(size.width(), size.height())
    window.resize(calculated_size[0], calculated_size[1])
    apply_stylesheet(app, theme='dark_amber.xml')
    window.show()
    sys.exit(app.exec_())
