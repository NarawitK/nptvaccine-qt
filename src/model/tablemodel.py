from PySide2.QtCore import Qt, QAbstractTableModel

class TableModel(QAbstractTableModel):

    def __init__(self, df):
        super().__init__()
        self.df = df

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self.df.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self.df.shape[0]

    def columnCount(self, index):
        return self.df.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.df.columns[section])

            if orientation == Qt.Vertical:
                return str(self.df.index[section])
