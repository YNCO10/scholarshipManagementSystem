from PyQt6.QtWidgets import QMainWindow, QHeaderView
from PyQt6 import uic

from SholarshipManagementSystem.homePage.dashboard import Ui_MainWindow


class Dash(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("C:/Users/Yankho/OneDrive/Desktop/PROJECT/SholarshipManagementSystem/homePage/dash.ui", self)
        self.setupUi(self)
        self.setWindowTitle("Dashboard.")

        self.iconNameWidget.setHidden(True)

        self.homeBtn.clicked.connect(self.switchToDash)
        self.homeIconBtn.clicked.connect(self.switchToDash)

        self.scholarshipBtn.clicked.connect(self.switchToScholarshipPage)
        self.scholarshipIconBtn.clicked.connect(self.switchToScholarshipPage)

        self.reportBtn.clicked.connect(self.switchToReportsPage)
        self.reportIconBtn.clicked.connect(self.switchToReportsPage)

        self.profileBtn.clicked.connect(self.switchToProfilePage)
        self.profileIconBtn.clicked.connect(self.switchToProfilePage)
        self.profileBtnQuickAccess.clicked.connect(self.switchToProfilePage)

        self.notificationsBtn.clicked.connect(self.switchToNotificationsPage)
        self.notificationsIconBtn.clicked.connect(self.switchToNotificationsPage)


        # # TABLE WIDGET RESIZING CODE
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #
        # self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #
        # self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #
        # self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


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
