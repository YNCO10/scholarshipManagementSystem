from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog

from SholarshipManagementSystem.dialogBox.confirmationBox import Ui_templateDialog

class ConfirmationBox(QDialog, Ui_templateDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))

    def btnClicks(self):
        if self.okCanelBtnBox.accepted:
            return True

        if self.okCanelBtnBox.rejected:
            return False