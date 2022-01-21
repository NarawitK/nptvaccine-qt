from PySide2.QtCore import Qt, QAbstractTableModel

class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self.dataa = data

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self.dataa.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self.dataa.shape[0]

    def columnCount(self, index):
        return self.dataa.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.dataa.columns[section])

            if orientation == Qt.Vertical:
                return str(self.dataa.index[section])