from modules.financial_filter import FinancialFilter
from modules.worker import FilterWorker
from components.filedialog import OpenSpreadSheetWidget, SaveSpreadsheetWidget
from PySide2 import QtCore, QtWidgets


class FinvacWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.pool = QtCore.QThreadPool()
        self.__has_save_path = False
        self.__has_file_path = False
        self.__file_path = None
        self.__save_path = None
        self.__started_filtering_text = "Reading & Writing . . ."
        self.__finished_filtering_text = "Done"
        self.__error_filtering_text = "Error: "
        self.render_components()

    def render_components(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.__fileopener = OpenSpreadSheetWidget("เลือกไฟล์วัคซีนรายวันจาก MOPH-IC")
        self.__filesaver = SaveSpreadsheetWidget()
        self.executeButton = QtWidgets.QPushButton("Conve&rt")
        self.status_label = QtWidgets.QLabel("สถานะ") 
        self.executeButton.setEnabled(False)
        self.status_text = QtWidgets.QTextEdit()
        self.status_text.setReadOnly(True)

        self.layout.addWidget(self.__fileopener)
        self.layout.addWidget(self.__filesaver)
        self.layout.addWidget(self.executeButton)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_text)
        self.__fileopener.fileChoose.connect(self.__setFilePath)
        self.__filesaver.saveLocationSelected.connect(self.__setSavePath)
        self.executeButton.clicked.connect(self.beginGenerateExcel)
        self.setLayout(self.layout)
    
    @QtCore.Slot(str, bool)
    def __setFilePath(self, path, hasPathSet):
        self.__has_file_path = hasPathSet
        if(hasPathSet):
            self.__file_path = path
        self.__enableRunWhenPathsSet()

    @QtCore.Slot(str, bool)
    def __setSavePath(self, path, hasPathSet):
        self.__has_save_path = hasPathSet
        if(hasPathSet):
            self.__save_path = path
        self.__enableRunWhenPathsSet()

    def __enableRunWhenPathsSet(self):
        if(self.__has_file_path and self.__has_save_path):
            self.executeButton.setEnabled(True)
        else:
            self.executeButton.setEnabled(False)

    @QtCore.Slot()
    def beginGenerateExcel(self):
        worker = FilterWorker(self.process_file, self.__started_filtering_text, self.__finished_filtering_text, self.__error_filtering_text, self.__file_path, self.__save_path)
        worker.signals.started.connect(self.start_reading)
        worker.signals.finished.connect(self.finished_reading)
        worker.signals.error.connect(self.finished_reading)
        self.pool.start(worker)

    def process_file(self, inPath, outPath):
        instance = FinancialFilter(inPath)
        instance.filter_date()
        instance.prepare_filtered_date_sheets()
        instance.write_to_excel(outPath)

    @QtCore.Slot(str)
    def finished_reading(self, msg):
        self.status_text.setText(msg)
        self.executeButton.setEnabled(True)
    
    @QtCore.Slot(str)
    def start_reading(self, msg):
        self.status_text.setText(msg)
        self.executeButton.setEnabled(False)
