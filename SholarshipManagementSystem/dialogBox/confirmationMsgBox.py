from PyQt6.QtWidgets import QMessageBox

class MsgBox:
    def __init__(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Confirm Action")
        self.msg.setText("Do you want to continue?")
        self.msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        self.msg.exec()
        self.btnClicks()

    def btnClicks(self):
        if QMessageBox.StandardButton.Ok:
            return True
        else:
            return False

msg = MsgBox()