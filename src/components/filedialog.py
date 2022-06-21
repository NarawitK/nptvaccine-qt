from PySide2 import QtCore, QtWidgets


class OpenSpreadSheetWidget(QtWidgets.QWidget):
    fileChoose = QtCore.Signal(str, bool)
    def __init__(self):
        super().__init__()
        self.render_component()

    def render_component(self):
        layout = QtWidgets.QVBoxLayout()
        filechooser_layout = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel("ไฟล์")
        self.path_textfield = QtWidgets.QLineEdit()
        self.path_textfield.setReadOnly(True)
        self.browse_file_button = QtWidgets.QPushButton("&Browse File")
        self.browse_file_button.clicked.connect(self.on_browse_button_clicked)

        layout.addWidget(self.file_label)
        filechooser_layout.addWidget(self.path_textfield)
        filechooser_layout.addWidget(self.browse_file_button)
        layout.addLayout(filechooser_layout)
        self.setLayout(layout)

    @QtCore.Slot()
    def on_browse_button_clicked(self):
        defaultpath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DesktopLocation)
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose your file", defaultpath, "Excel 2010+ (*xlsx);;csv (*.csv)")
        if(filePath is not None and filePath != ''):
            self.path_textfield.setText(filePath)
            self.fileChoose.emit(filePath, True)
        else:
            self.fileChoose.emit(filePath, False)
            self.path_textfield.setText("Choose your file")


class SaveSpreadsheetWidget(QtWidgets.QWidget):
    saveLocationSelected = QtCore.Signal(str, bool)
    def __init__(self):
        super().__init__()
        self.render_component()

    def render_component(self):
        layout = QtWidgets.QVBoxLayout()
        save_widget_layout = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel("ตำแหน่งที่ต้องการเซฟไฟล์")
        self.path_textfield = QtWidgets.QLineEdit()
        self.path_textfield.setReadOnly(True)
        self.browse_file_button = QtWidgets.QPushButton("&Save As")
        self.browse_file_button.clicked.connect(self.on_browse_button_clicked)

        layout.addWidget(self.file_label)
        save_widget_layout.addWidget(self.path_textfield)
        save_widget_layout.addWidget(self.browse_file_button)
        layout.addLayout(save_widget_layout)
        self.setLayout(layout)

    @QtCore.Slot()
    def on_browse_button_clicked(self):
        defaultpath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DesktopLocation)
        savePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Choose where to save", defaultpath, "Excel 2010+ (*.xlsx)")
        if(savePath is not None and savePath != ''):
            self.path_textfield.setText(savePath)
            self.saveLocationSelected.emit(savePath, True)
        else:
            self.saveLocationSelected.emit(savePath, False)
            self.path_textfield.setText("Choose your save location")