import webbrowser
from helper import helper
from PySide2 import QtCore, QtWidgets
from components.filedialog import OpenSpreadSheetWidget
from modules.dailyfilter import DailyFilter, DocuChecker
from modules.worker import FilterWorker
from model.tablemodel import TableModel


class DailyFilterWidget(QtWidgets.QWidget):
    dataready = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.df = None
        self.file_path = None
        self.render_component()
        self.pool = QtCore.QThreadPool()
        self.__started_filtering_text = "Reading. . ."
        self.__finished_filtering_text = "กด Ctrl+Shift+V ที่ Cell ที่ต้องการวางข้อมูลใน G. Sheet NPTVaccine"
        self.__error_filtering_text = "Error: "
        
    def render_component(self):
        self.layout = QtWidgets.QVBoxLayout()
        #File Chooser Widget
        self.filechooser = OpenSpreadSheetWidget()

        #Runner Widgets
        self.status_label = QtWidgets.QLabel("สถานะ")
        self.status_textfield = QtWidgets.QLineEdit()
        self.status_textfield.setReadOnly(True)
        self.run_button = QtWidgets.QPushButton("&Run")
        self.run_button.setEnabled(False)
        self.web_button = QtWidgets.QPushButton("Go to NPTVaccine &Web")
        self.table_label = QtWidgets.QLabel("ตารางสรุปข้อมูล")
        self.tableview = QtWidgets.QTableView()

        self.layout.addWidget(self.filechooser)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_textfield)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.web_button)
        self.layout.addWidget(self.table_label)
        self.layout.addWidget(self.tableview)

        #Signal-Slot Connect
        self.run_button.clicked.connect(self.on_run_button_clicked)
        self.web_button.clicked.connect(self.on_web_button_clicked)
        self.dataready.connect(self.setup_table_model)
        self.filechooser.fileChoose.connect(self.on_file_chosen)

        self.setLayout(self.layout)

    @QtCore.Slot(str, bool)
    def on_file_chosen(self, filepath, isFileChoosen):
        if isFileChoosen:
            self.file_path = filepath
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)


    @QtCore.Slot()
    def on_run_button_clicked(self):
        file_path = self.filechooser.path_textfield.text()
        if file_path is not None:
            self.run_button.setEnabled(False)
            self.start_worker(self.file_path)
        else:
            self.status_textfield.setText("ยังไม่ได้เลือกไฟล์ต้นฉบับ")

    @QtCore.Slot()
    def on_web_button_clicked(self):
        try:
            url = helper.read_config()['npt_url']
            webbrowser.open(url)
        except:
            self.status_textfield.setText("ไม่มี Browser ติดตั้งบนคอมพิวเตอร์")
    
    @QtCore.Slot(str)
    def start_worker(self, filepath):
        worker = FilterWorker(self.start_procedure, self.__started_filtering_text, self.__finished_filtering_text, self.__error_filtering_text, filepath)
        worker.signals.started.connect(self.finished_reading)
        worker.signals.finished.connect(self.finished_reading)
        worker.signals.error.connect(self.on_finish_with_error)
        self.pool.start(worker)

    def start_procedure(self, filePath):
        instance = DailyFilter(filePath)
        errorcheck_result = self.__check_source_for_error(instance.get_dataframe())
        if errorcheck_result is not None:
            raise ValueError(errorcheck_result.exception_message)
        else:
            instance.prepareData()
            df = instance.export_df_for_npt()
            table_df = instance.export_tabular_df()
            self.df = table_df
            table_model = TableModel(table_df)     
            self.dataready.emit(table_model)
            instance.to_clipboard(df) 

    def __check_source_for_error(self, source_df):
        checker_instance = DocuChecker(source_df)
        if checker_instance.get_has_error():
            error_df = checker_instance.get_error_details()
            error_count = error_df.shape[0]
            table_df = error_df
            group_error_model = TableModel(table_df)
            self.dataready.emit(group_error_model)
            exception_string = 'พบข้อผิดพลาดที่กลุ่มเป้าหมาย จำนวน ' + str(error_count) + ' รายการ '
            error_detail = GroupErrorModel(True, exception_string)
            return error_detail
        else:
            return None

    @QtCore.Slot(object)
    def setup_table_model(self, model):
        self.tableview.setModel(model)
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
    
    @QtCore.Slot(str)
    def finished_reading(self, message):
        self.status_textfield.setText(message)        
        self.run_button.setEnabled(True)

    @QtCore.Slot(str)
    def on_finish_with_error(self, message):
        self.status_textfield.setText(message)
        self.run_button.setEnabled(True)


class GroupErrorModel:
    def __init__(self):
        self.__has_error = None
        self.__exception_message = None

    def __init__(self, has_error, exception_message):
        self.__has_error = has_error
        self.__exception_message = exception_message

    @property
    def has_error(self):
        return self.__has_error

    @property
    def exception_message(self):
        return self.__exception_message

    @has_error.setter
    def has_error(self, value):
        self.__has_error = value

    @exception_message.setter
    def exception_message(self, msg):
        self.__exception_message = msg

