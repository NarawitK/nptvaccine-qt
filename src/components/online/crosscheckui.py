from PySide2 import QtWidgets


class CrossCheckComponent(QtWidgets.QWidget):
    def __init__(self, main_window, token_manager):
        super(CrossCheckComponent, self).__init__()
        self._main_window = main_window
        self._token_manager = token_manager
        self.__render_component()

    def __render_component(self):
        # Declare Layout
        layout = QtWidgets.QGridLayout()

        self.startdate_lbl = QtWidgets.QLabel("StartDate")
        self.startdate_cl = QtWidgets.QDateEdit()
        self.enddate_lbl = QtWidgets.QLabel("End Date")
        self.enddate_cl = QtWidgets.QDateEdit()
        self.samedate_lbl = QtWidgets.QLabel("Is Same Date")
        self.samedate_cb = QtWidgets.QCheckBox("Same &Date")
        self.confirm_btn = QtWidgets.QPushButton("&Start Search")
        self.tableview = QtWidgets.QTableView()

        # self.confirm_btn.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding)
        # self.tableview.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding)

        layout.addWidget(self.startdate_lbl, 0, 0)
        layout.addWidget(self.startdate_cl, 0, 1)
        layout.addWidget(self.enddate_lbl, 1, 0)
        layout.addWidget(self.enddate_cl, 1, 1)
        layout.addWidget(self.samedate_lbl, 2, 0)
        layout.addWidget(self.samedate_cb, 2, 1)
        # (row, col, rspan, cspan)
        layout.addWidget(self.confirm_btn, 3, 0, 3, 1)
        layout.addWidget(self.tableview, 4, 0, 4, 2)

        layout.setColumnStretch(1, 3)

        self.setLayout(layout)
