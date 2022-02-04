from PySide2 import QtCore, QtWidgets
from components.filedialog import OpenSpreadSheetWidget
from modules.worker import FilterWorker
from model.tablemodel import TableModel
from modules.weeklyfilter import WeeklyFilter

class WeeklyFilterWidget(QtWidgets.QWidget):
    tablemodelready = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.file_path = None
        self.render_component()
        self.pool = QtCore.QThreadPool()
        self.__started_filtering_text = "Reading. . ."
        self.__finished_filtering_text = "Done"
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
        self.table_label = QtWidgets.QLabel("ตารางสรุปข้อมูล")
        self.tableview = QtWidgets.QTableView()

        self.layout.addWidget(self.filechooser)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_textfield)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.table_label)
        self.layout.addWidget(self.tableview)

        #Signal-Slot Connect
        self.run_button.clicked.connect(self.on_run_button_clicked)
        self.tablemodelready.connect(self.setup_table_model)
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
    
    @QtCore.Slot(str)
    def start_worker(self, filepath):
        worker = FilterWorker(self.start_procedure, self.__started_filtering_text, self.__finished_filtering_text, self.__error_filtering_text, filepath)
        worker.signals.started.connect(self.finished_reading)
        worker.signals.finished.connect(self.finished_reading)
        worker.signals.error.connect(self.on_finish_with_error)
        self.pool.start(worker)
    
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

    def start_procedure(self, filePath):
        instance = WeeklyFilter(filePath)
        table_model = TableModel(instance.df)
        self.tablemodelready.emit(table_model)
        
        # TODO: Add group checker for weekly vaccine list
        # Below this comment line

        
'''
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
'''
