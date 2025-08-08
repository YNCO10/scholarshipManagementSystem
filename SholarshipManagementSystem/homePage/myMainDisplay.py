from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QDialog, QLineEdit
from PyQt6 import uic

from SholarshipManagementSystem.homePage.dashboard import Ui_MainWindow
from SholarshipManagementSystem.manageScholarshipsPage.uploadScholarships import Ui_Dialog


class Dash(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("C:/Users/Yankho/OneDrive/Desktop/PROJECT/SholarshipManagementSystem/homePage/dash.ui", self)
        self.setupUi(self)
        self.setWindowTitle("Dashboard.")

        self.passTxt.setText("THIS IS A RANDOM PASSWORD NIGGA")

        #DISPLAY HOME SCREEN
        self.mainDisplayWidget.setCurrentIndex(0)
        self.homeBtn.click()
        self.homeIconBtn.click()

        self.iconNameWidget.setHidden(True)

        # NAV BAR BTN CLICKS
        self.BtnClicks()

    #BTN CLICKS
    def BtnClicks(self):
        # Home
        self.homeBtn.clicked.connect(self.switchToDash)
        self.homeIconBtn.clicked.connect(self.switchToDash)
        # scholar...
        self.scholarshipBtn.clicked.connect(self.switchToScholarshipPage)
        self.scholarshipIconBtn.clicked.connect(self.switchToScholarshipPage)
        # report
        self.reportBtn.clicked.connect(self.switchToReportsPage)
        self.reportIconBtn.clicked.connect(self.switchToReportsPage)
        # profile
        self.profileBtn.clicked.connect(self.switchToProfilePage)
        self.profileIconBtn.clicked.connect(self.switchToProfilePage)
        self.profileBtnQuickAccess.clicked.connect(self.switchToProfilePage)
        # noti...
        self.notificationsBtn.clicked.connect(self.switchToNotificationsPage)
        self.notificationsIconBtn.clicked.connect(self.switchToNotificationsPage)
        # scholarshipDialog
        self.uploadScholarshipBtn.clicked.connect(self.goToUploadScholarship)
    #     show password
        self.showPassBtn.clicked.connect(self.togglePasswordBtn)


    def goToUploadScholarship(self):
        dialog = QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog)

        ui.cancelBtn.clicked.connect(dialog.close)#close dialog

        dialog.exec()


    def togglePasswordBtn(self):
        if self.passTxt.echoMode() == QLineEdit.EchoMode.Normal:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Password)
            self.showPassBtn.setIcon(QIcon("icons/seeWhiteIcon.png"))
        else:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.showPassBtn.setIcon(QIcon("icons/hideWhite.png"))


    # PAGE SWITCHING
    def switchToDash(self):
        self.mainDisplayWidget.setCurrentIndex(0)

    def switchToScholarshipPage(self):
        self.mainDisplayWidget.setCurrentIndex(1)

    def switchToNotificationsPage(self):
        self.mainDisplayWidget.setCurrentIndex(3)

    def switchToProfilePage(self):
        self.mainDisplayWidget.setCurrentIndex(2)

    def switchToReportsPage(self):
        self.mainDisplayWidget.setCurrentIndex(4)

    def goToUploadScholarShipsPage(self):
        self.uploadScholarshipBtn.clicked.connect()
    # PAGE SWITCHING END
