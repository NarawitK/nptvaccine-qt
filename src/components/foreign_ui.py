from PySide2 import QtCore, QtWidgets
from components.filedialog import OpenSpreadSheetWidget, SaveSpreadsheetWidget
from datafetch.dbconnector import MariaDBConnector
from datafetch.hosxp_dataaccess import HosxpDataAccess
from modules.foreignfilter import ForeignFilter
from modules.worker import FilterWorker


class ForeignWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = None
        self.pool = QtCore.QThreadPool()
        self.__has_save_path = False
        self.__has_file_path = False
        self.__file_path = None
        self.__save_path = None
        self.render_components()

    def render_components(self):
        # Layout
        self.__layout = QtWidgets.QVBoxLayout(self)
        self.__calendar_layout = QtWidgets.QHBoxLayout()
        self.__calendar_widget = QtWidgets.QWidget()
        self.__startdate_layout = QtWidgets.QVBoxLayout()
        self.__enddate_layout = QtWidgets.QVBoxLayout()

        self.__fileopen_widget = OpenSpreadSheetWidget("เลือกไฟล์กลุ่มเป้าหมายที่ดาวน์โหลดจาก MOPH-IC")
        self.__savefile_widget = SaveSpreadsheetWidget("ตำแหน่งที่ต้องการบันทึกไฟล์")
        self.__filter_prefecture_checkbox = QtWidgets.QCheckBox("กรองที่อยู่เฉพาะ ต.กำแพงแสน อ.กำแพงแสน จ.นครปฐม")
        self.__filter_prefecture_checkbox.setToolTip("ติ๊กเพื่อกรอง")
        self.__startdate_lbl = QtWidgets.QLabel("เลือกวันเริ่มต้น")
        self.__startdate_dp = QtWidgets.QCalendarWidget()
        self.__enddate_lbl = QtWidgets.QLabel("เลือกวันสิ้นสุด")
        self.__enddate_dp = QtWidgets.QCalendarWidget()
        self.__enddate_dp.setMinimumDate(self.__startdate_dp.selectedDate())
        self.__export_button = QtWidgets.QPushButton("&Export")
        self.__export_button.setEnabled(False)
        self.__status_label = QtWidgets.QLabel("สถานะ")
        self.__status_text = QtWidgets.QTextEdit()
        self.__status_text.setReadOnly(True)

        self.__layout.addWidget(self.__fileopen_widget)
        self.__layout.addWidget(self.__savefile_widget)
        self.__layout.addWidget(self.__filter_prefecture_checkbox)
        # Add Calendar Sub-Layout
        self.__startdate_layout.addWidget(self.__startdate_lbl)
        self.__startdate_layout.addWidget(self.__startdate_dp)
        self.__enddate_layout.addWidget(self.__enddate_lbl)
        self.__enddate_layout.addWidget(self.__enddate_dp)
        self.__calendar_layout.addLayout(self.__startdate_layout)
        self.__calendar_layout.addLayout(self.__enddate_layout)
        self.__calendar_widget.setLayout(self.__calendar_layout)
        # End
        self.__layout.addWidget(self.__calendar_widget)
        self.__layout.addWidget(self.__export_button)
        self.__layout.addWidget(self.__status_label)
        self.__layout.addWidget(self.__status_text)

        self.__fileopen_widget.fileChoose.connect(self.__setFilePath)
        self.__savefile_widget.saveLocationSelected.connect(self.__setSavePath)
        self.__export_button.clicked.connect(self.init_export)
        self.__startdate_dp.selectionChanged.connect(self.on_startdate_selection_changed)
        self.setLayout(self.__layout)

    @QtCore.Slot()
    def init_export(self):
        worker = FilterWorker(self.filter_then_export, "กำลังกรอกข้อมูล ระหว่างนี้ทำงานอื่นรอไปก่อนได้เลย", "เสร็จสิ้นกระบวนการ", "เกิดข้อผิดพลาด", self.__file_path, self.__save_path, self.__get_filter_prefecture_checked_status())
        worker.signals.started.connect(self.start_reading)
        worker.signals.error.connect(self.finished_reading)
        worker.signals.finished.connect(self.finished_reading)
        self.pool.start(worker)

    @QtCore.Slot()
    def on_startdate_selection_changed(self):
        start_date = self.__startdate_dp.selectedDate()
        self.__enddate_dp.setMinimumDate(start_date)

    def filter_then_export(self, group_source_path, output_path, filter_prefecture):
        start_date = self.__startdate_dp.selectedDate().toPython()
        end_date = self.__enddate_dp.selectedDate().toPython()
        filter_instance = ForeignFilter(group_source_path, filter_prefecture)
        with MariaDBConnector().get_instance() as connection_instance:
            hosxp_vaccinate_list = HosxpDataAccess(connection_instance).query_injection_by_visitdate(start_date,
                                                                                                     end_date)
            filter_instance.convert_hosxp_to_df(hosxp_vaccinate_list)
        result_dataframe = filter_instance.merge_dataframes(filter_instance.hosxp_df, filter_instance.mophic_df)
        filter_instance.export_to_excel(output_path, result_dataframe)

    @QtCore.Slot(str, bool)
    def __setFilePath(self, path, is_path_set):
        self.__has_file_path = is_path_set
        if is_path_set:
            self.__file_path = path
        self.__enableRunWhenPathsSet()

    @QtCore.Slot(str, bool)
    def __setSavePath(self, path, is_path_set):
        self.__has_save_path = is_path_set
        if is_path_set:
            self.__save_path = path
        self.__enableRunWhenPathsSet()

    @QtCore.Slot(str)
    def start_reading(self, msg):
        self.__status_text.setText(msg)
        self.__export_button.setEnabled(False)

    @QtCore.Slot(str)
    def finished_reading(self, msg):
        self.__status_text.setText(msg)
        self.__export_button.setEnabled(True)

    def __enableRunWhenPathsSet(self):
        if self.__has_file_path and self.__has_save_path:
            self.__export_button.setEnabled(True)
        else:
            self.__export_button.setEnabled(False)

    def __get_filter_prefecture_checked_status(self):
        return self.__filter_prefecture_checkbox.isChecked()