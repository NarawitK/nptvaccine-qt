from PySide2 import QtWidgets, QtCore


class DoseSpinner(QtWidgets.QWidget):
    onMinDoseChanged = QtCore.Signal(int)
    onMaxDoseChanged = QtCore.Signal(int)

    def __init__(self, min_dose: int = 1, max_dose: int = 2) -> None:
        super().__init__()
        self.__main_grid = None
        self.min_dose_label = None
        self.max_dose_label = None
        self.min_dose_spinner = None
        self.max_dose_spinner = None
        self.__render_components(min_dose, max_dose)

    def __render_components(self, min_dose: int = 1, max_dose: int = 2):
        self.__main_grid = QtWidgets.QGridLayout(self)
        # Widget Declaration
        self.min_dose_label = QtWidgets.QLabel("เริ่มต้นที่ Dose")
        self.max_dose_label = QtWidgets.QLabel("ถึง Dose ที่")
        self.min_dose_spinner = QtWidgets.QSpinBox()
        self.min_dose_spinner.setValue(min_dose)
        self.min_dose_spinner.setMinimum(1)
        self.min_dose_spinner.valueChanged.connect(self.on_min_dose_value_changed)
        self.max_dose_spinner = QtWidgets.QSpinBox()
        self.max_dose_spinner.setValue(max_dose)
        self.max_dose_spinner.setMinimum(min_dose)
        self.max_dose_spinner.valueChanged.connect(self.on_max_dose_value_changed)

        # Set Layout
        self.__main_grid.addWidget(self.min_dose_label, 0, 0)
        self.__main_grid.addWidget(self.max_dose_label, 0, 1)
        self.__main_grid.addWidget(self.min_dose_spinner, 1, 0)
        self.__main_grid.addWidget(self.max_dose_spinner, 1, 1)

    def get_doses(self) -> dict:
        return {"min_dose": self.min_dose_spinner.value(), "max_dose": self.max_dose_spinner.value()}

    # Spinner Slot
    def on_min_dose_value_changed(self):
        min_dose = self.min_dose_spinner.value()
        max_dose = self.max_dose_spinner.value()
        self.onMinDoseChanged.emit(min_dose)
        if min_dose > max_dose:
            self.max_dose_spinner.setMinimum(min_dose)
        else:
            self.max_dose_spinner.setMinimum(min_dose)

    def on_max_dose_value_changed(self):
        max_dose = self.max_dose_spinner.value()
        self.onMaxDoseChanged.emit(max_dose)
