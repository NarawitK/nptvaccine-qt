from PySide2.QtWidgets import QMessageBox


def show_msg_box(severity: QMessageBox, header, message):
    msgBox = QMessageBox()
    msgBox.setIcon(severity)
    msgBox.setText(header)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    msgBox.exec()
