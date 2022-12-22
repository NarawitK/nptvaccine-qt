import constant
from PySide2 import QtWidgets
from components.dailyui import DailyFilterWidget
from components.groupfilterui import VaccineGroupingSummary
from components.finvac_ui import FinvacWidget
from components.weeklyui import WeeklyFilterWidget
from components.foreign_ui import ForeignWidget
from components.settings.daily.daily_setting_ui import DailySettingWidget
from components.settings.weekly.weekly_setting_ui import WeeklySettingWidget
from components.settings.person.person_setting_ui import PersonTypeSettingWidget


class MainMenuTabWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QtWidgets.QVBoxLayout()
        self.__main_tabs = None
        self.__func_tabs = None
        self.__setting_tabs = None
        self.__invoke_app_instances()
        self.__construct_main_tabs()

    def __invoke_app_instances(self):
        self.__daily_filter_screen = DailyFilterWidget()
        self.__vac_group_screen = VaccineGroupingSummary()
        self.__fin_vac_screen = FinvacWidget()
        self.__weekly_group_screen = WeeklyFilterWidget()
        self.__foreign_filter_screen = ForeignWidget()
        self.__daily_setting_screen = DailySettingWidget()
        self.__weekly_setting_screen = WeeklySettingWidget()
        self.__person_type_setting_screen = PersonTypeSettingWidget()

    def __construct_main_tabs(self):
        self.__main_tabs = QtWidgets.QTabWidget()
        self.__construct_functions_tab()
        self.__construct_settings_tab()
        self.__main_tabs.addTab(self.__func_tabs, constant.MAIN_FUNC_TAB_NAME)
        self.__main_tabs.addTab(self.__setting_tabs, constant.SETTING_TAB_NAME)
        self.__layout.addWidget(self.__main_tabs)
        self.setLayout(self.__layout)

    def __construct_functions_tab(self):
        self.__func_tabs = QtWidgets.QTabWidget()
        self.__func_tabs.addTab(self.__daily_filter_screen, constant.DAILY_VACCINE_REPORT_TAB_NAME)
        self.__func_tabs.addTab(self.__vac_group_screen, constant.DAILY_SEPARATE_REPORT_TAB_NAME)
        self.__func_tabs.addTab(self.__weekly_group_screen, constant.WEEKLY_PERSON_VAC_REPORT_TAB_NAME)
        self.__func_tabs.addTab(self.__fin_vac_screen, constant.FINANCIAL_REPORT_TAB_NAME)
        self.__func_tabs.addTab(self.__foreign_filter_screen, constant.FOREIGN_NON_THAI_REPORT_TAB_NAME)

    def __construct_settings_tab(self):
        self.__setting_tabs = QtWidgets.QTabWidget()
        self.__setting_tabs.addTab(self.__person_type_setting_screen, constant.PERSON_TYPE_SETTING_TAB_NAME)
        self.__setting_tabs.addTab(self.__daily_setting_screen, constant.DAILY_VACCINE_REPORT_SETTING_TAB_NAME)
        self.__setting_tabs.addTab(self.__weekly_setting_screen, constant.WEEKLY_PERSON_VAC_REPORT_SETTING_TAB_NAME)
