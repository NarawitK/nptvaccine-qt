import webbrowser
from helper import helper
from PySide2 import QtCore, QtWidgets
from components.filedialog import OpenSpreadSheetWidget
from modules.dailyfilter import DailyFilter
from modules.worker import FilterWorker
from model.tablemodel import TableModel

class DailyFilterWidget(QtWidgets.QWidget):
    #fileChoose = QtCore.Signal(str)
    dataready = QtCore.Signal(object)
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.render_component()
        self.pool = QtCore.QThreadPool()
        self.__started_filtering_text = "Reading. . ."
        self.__finished_filtering_text = "กด Ctrl+Shift+V ที่ Cell ที่ต้องการวางข้อมูลใน G. Sheet NPTVaccine"
        self.__error_filtering_text = "Error ถ่ายรูปเก็บไว้แจ้งก็ดีนะ: "
        
    def render_component(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.filechooser_layout = QtWidgets.QHBoxLayout()
        #File Chooser Widget
        self.filechooser = OpenSpreadSheetWidget()

        #Runner Widgets
        self.status_label = QtWidgets.QLabel("สถานะ")
        self.status_textfield = QtWidgets.QLineEdit()
        self.status_textfield.setReadOnly(True)
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.setEnabled(False)
        self.web_button = QtWidgets.QPushButton("Go to NPTVaccine Web")
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
        self.dataready.connect(self.setupTableModel)        
        self.filechooser.fileChoose.connect(self.on_file_chosen)

        self.setLayout(self.layout)

    @QtCore.Slot(str, bool)
    def on_file_chosen(self, filepath, isFileChoosen):
        if(isFileChoosen):
            self.file_path = filepath
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)

    @QtCore.Slot()
    def on_run_button_clicked(self):
        file_path = self.filechooser.path_textfield.text()
        if(file_path is not None):
            self.run_button.setEnabled(False)
            self.start_worker(self.file_path)
        else:
            self.status_textfield.setText("No file path yet.")

    @QtCore.Slot()
    def on_web_button_clicked(self):
        try:
            url = helper.read_config()['npt_url']
            webbrowser.open(url)
        except:
            self.status_textfield.setText("คอมคุณไม่มี Browser งั้นหรือ หืม ??")
    
    @QtCore.Slot(str)
    def start_worker(self, filepath):
        worker = FilterWorker(self.readSheet, self.__started_filtering_text, self.__finished_filtering_text, self.__error_filtering_text, filepath)
        worker.signals.started.connect(self.finished_reading)
        worker.signals.finished.connect(self.finished_reading)
        worker.signals.error.connect(self.finished_reading)
        self.pool.start(worker)

    def readSheet(self, filePath):
        instance = DailyFilter()
        instance.readSpreadSheet(filePath)
        instance.prepareData()
        df = instance.export_df_for_npt()
        table_df = instance.export_tabular_df()
        table_model = TableModel(table_df)     
        self.dataready.emit(table_model)
        instance.to_clipboard(df)

    @QtCore.Slot(object)
    def setupTableModel(self, model):
        self.tableview.setModel(model)
    
    @QtCore.Slot(str)
    def finished_reading(self, filePath):
        self.status_textfield.setText(filePath)
        self.run_button.setText("Run")
        self.run_button.setEnabled(True)