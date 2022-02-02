from PySide2 import QtCore, QtWidgets
from components.filedialog import OpenSpreadSheetWidget
from modules.groupfilter import GroupFilter
from model.tablemodel import TableModel
from modules.worker import FilterWorker

class VaccineGroupingSummary(QtWidgets.QWidget):
    begin_setup_datatable = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.table_model = None
        self.render_components()
        self.begin_setup_datatable.connect(self.setupTableModel)
        self.pool = QtCore.QThreadPool()
        self.__started_filtering_text = "Reading. . ."
        self.__finished_filtering_text = "คลิกเลือก Cell(s) จากนั้นดูผลรวมในช่อง 'ผลรวม'"
        self.__error_filtering_text = "Error: "

    def render_components(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.filechooser = OpenSpreadSheetWidget()
        self.status_label = QtWidgets.QLabel("สถานะ")
        self.status_text = QtWidgets.QLineEdit()
        self.status_text.setPlaceholderText("เลือกไฟล์ > Run > คลิก/ลากข้อมูลใน Cell ตาราง เพื่ออ่านผลรวม")
        self.status_text.setReadOnly(True)
        self.run_button = QtWidgets.QPushButton("&Run")
        self.run_button.setEnabled(False)
        self.sum_label = QtWidgets.QLabel("ผลรวม")
        self.sum_text = QtWidgets.QLineEdit('0')
        self.sum_text.setReadOnly(True)
        self.summary_label = QtWidgets.QLabel("ตารางสรุปข้อมูล")
        self.tableview = QtWidgets.QTableView()

        self.layout.addWidget(self.filechooser)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_text)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.sum_label)
        self.layout.addWidget(self.sum_text)
        self.layout.addWidget(self.summary_label)
        self.layout.addWidget(self.tableview)
        self.filechooser.fileChoose.connect(self.on_file_chosen)
        self.run_button.clicked.connect(self.onRunButtonPressed)
        self.setLayout(self.layout)
        
    
    @QtCore.Slot(str, bool)
    def on_file_chosen(self, filepath, isFileChoosen):
        if(isFileChoosen):
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)
    
    def onRunButtonPressed(self):
        self.run_button.setEnabled(False)
        self.sum_text.setText('0')
        worker = FilterWorker(self.parse_data_from_file, self.__started_filtering_text, self.__finished_filtering_text, self.__error_filtering_text, self.filechooser.path_textfield.text())
        worker.signals.started.connect(self.onFinishedReading)
        worker.signals.finished.connect(self.onFinishedReading)
        worker.signals.error.connect(self.onFinishedReading)
        self.pool.start(worker)

    def parse_data_from_file(self, filepath):
        instance = GroupFilter(filepath)
        instance.filter_vaccine_group()
        df = instance.export_tabular_df()
        self.begin_setup_datatable.emit(df)

    @QtCore.Slot(object)
    def setupTableModel(self, dataframe):
        self.table_model = TableModel(dataframe)
        self.tableview.setModel(self.table_model)
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
        self.tableview.selectionModel().selectionChanged.connect(self.sel_sum)

    @QtCore.Slot(str)
    def onFinishedReading(self, msg):
        self.setStatusText(msg)
        self.run_button.setEnabled(True)

    def setStatusText(self, text):
        self.status_text.setText(text)

    def sel_sum(self, selected, deselected):
        result = 0
        for index in sorted(self.tableview.selectedIndexes()):
            cell_data = self.table_model.data(self.table_model.index(index.row(), index.column()))
            result += int(cell_data)
        self.sum_text.setText(str(result))
        '''
        rows = sorted(set(index.row() for index in self.tableview.selectedIndexes()))
        cols = sorted(set(index.column() for index in self.tableview.selectedIndexes()))
        for row in rows:
            for col in cols:
                temp_sum = self.table_model.data(self.table_model.index(row, col))
                result += int(temp_sum)
        '''