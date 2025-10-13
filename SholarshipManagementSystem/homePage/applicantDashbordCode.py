import json
import os
import subprocess
import sys

import requests
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTableWidgetItem, QPushButton
from PyQt6.QtGui import QIcon

import Sessions
from SholarshipManagementSystem.homePage.applicantDashbord import Ui_ApplicantDash
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode


class ApplicantDash(QMainWindow, Ui_ApplicantDash):
    def __init__(self):
        super().__init__()
        self.notiDisplay = None
        self.regCode = RegCode()
        self.controller = None
        self.setupUi(self)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))

        # DISPLAY HOME SCREEN
        self.mainDisplayWidget.setCurrentIndex(0)
        self.homeBtn.setChecked(True)
        self.homeIconBtn.setChecked(True)
        #HIDE SIDEBAR
        self.iconNameWidget.setVisible(False)

        #btn clicks
        self.btnClicks()

########################################################################################################################
    def btnClicks(self):
        #home
        self.homeBtn.clicked.connect(self.switchToDash)
        self.homeIconBtn.clicked.connect(self.switchToDash)
        # scholar...
        self.scholarshipBtn.clicked.connect(self.switchToScholarships)
        self.scholarshipIconBtn.clicked.connect(self.switchToScholarships)
        #reports
        self.reportBtn.clicked.connect(self.switchToReports)
        self.reportIconBtn.clicked.connect(self.switchToReports)
        #noti...
        self.notificationsBtn.clicked.connect(self.switchToNotifications)
        self.notificationsIconBtn.clicked.connect(self.switchToNotifications)
        #profile
        self.profileBtn.clicked.connect(self.switchToProfile)
        self.profileIconBtn.clicked.connect(self.switchToProfile)
        self.profileBtnQuickAccess.clicked.connect(self.switchToProfile)

        #filter notification page
        self.noftiFilterbtn.clicked.connect(
            lambda : self.populateNotificationTbl(self.notiFilterCombo.currentText().strip())
        )

########################################################################################################################
    def switchToDash(self):
        self.mainDisplayWidget.setCurrentIndex(0)

    def switchToScholarships(self):
        self.mainDisplayWidget.setCurrentIndex(1)
        self.populateScholarshipTbl()

    def switchToReports(self):
        self.mainDisplayWidget.setCurrentIndex(2)

    def switchToNotifications(self):
        self.mainDisplayWidget.setCurrentIndex(3)
        self.populateNotificationTbl("All")

    def switchToProfile(self):
        self.mainDisplayWidget.setCurrentIndex(4)

########################################################################################################################
    def populateScholarshipTbl(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/getScholarshipDetails.php"
            )

            print(f"RAW RESPONSE: {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown response")

            if result.get("status") == "success":
                #     get db content
                dbContent = result.get("data", [])
                self.scholarshipTableWidget.setRowCount(
                    len(dbContent))  #always initialise tbl so it doesn't stack up rows
                Sessions.scholarshipCount = len(dbContent)

                self.scholarshipTableWidget.setColumnCount(13)

                self.scholarshipTableWidget.setHorizontalHeaderLabels(
                    [
                        "Actions",
                        "ID",
                        "Name",
                        "Descrip",
                        "Type",
                        "Subject",
                        "Deadline",
                        "Financial Amount",
                        "Provider",
                        "Provider Email",
                        "Application Link",
                        "Perks",
                        "File Path"
                    ]
                )

                #     populate tbl with content from db
                for rowindx, rowData in enumerate(dbContent):
                    #         fill data for all 4 columns
                    self.scholarshipTableWidget.setItem(rowindx, 1, QTableWidgetItem(str(rowData.get("id", ""))))
                    self.scholarshipTableWidget.setItem(rowindx, 2,
                                                        QTableWidgetItem(rowData.get("scholarship_name", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 3, QTableWidgetItem(rowData.get("descrip", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 4, QTableWidgetItem(rowData.get("type", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 5, QTableWidgetItem(rowData.get("subject", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 6, QTableWidgetItem(rowData.get("deadline", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 7,
                                                        QTableWidgetItem(rowData.get("financial_amount", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 8, QTableWidgetItem(rowData.get("provider", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 9, QTableWidgetItem(rowData.get("provider_email", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 10,
                                                        QTableWidgetItem(rowData.get("applicantion_link", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 11, QTableWidgetItem(
                        rowData.get("perks", "") or "No Benefits Available for this Scholarship"))
                    self.scholarshipTableWidget.setItem(rowindx, 12, QTableWidgetItem(rowData.get("file_path", "")))

                    #       create View & del btn
                    viewBtn = QPushButton("View")
                    applyBtn = QPushButton("Apply")

                    viewBtn.setStyleSheet("QPushButton { "
                                          "color: white;"
                                          "padding:3px;"
                                          "margin:0px;"
                                          "border-radius:3px;"
                                          "}")
                    applyBtn.setStyleSheet("QPushButton { "
                                           "color: white;"
                                           "padding:3px;"
                                           "margin:0px;"
                                           "border-radius:3px;"
                                           "}")

                    viewBtn.clicked.connect(
                        lambda _, path=rowData.get("file_path"): self.displayScholarshipDoc(path)
                    )
                    applyBtn.clicked.connect(
                        lambda _, Id=rowData.get("id"): self.showApplyScholarship(Id)
                    )

                    #   align horizontally
                    btnWidget = QWidget()
                    layout = QHBoxLayout(btnWidget)
                    layout.addWidget(applyBtn)
                    layout.addWidget(viewBtn)
                    layout.setContentsMargins(0, 0, 0, 0)

                    #         add widget to tbl
                    self.scholarshipTableWidget.setCellWidget(rowindx, 0, btnWidget)

                self.styleTbl(self.scholarshipTableWidget)

            elif result.get("message") == "error":
                self.regCode.msgBox("Error(ScholarTbl)", f"Error: {msg}")
                print(msg)

        except Exception as e:
            self.regCode.msgBox("Error", f"Something went wrong Populating scholarships tbl(dash): {e}")
            print(e)

########################################################################################################################
    def displayScholarshipDoc(self, path):

        print(repr(path))
        # referenceDir = "C:/XAMPP/htdocs/BackEnd/scholarshipManagement/uploadScholarships/docs/uploadedFiles"
        xamppDir = r"C:/XAMPP/htdocs/BackEnd/scholarshipManagement/uploadScholarships/docs/uploadedFiles"

        fullPath = os.path.join(xamppDir, path)

        fullPath = os.path.normpath(fullPath)

        print(fullPath)
        os.startfile(fullPath)

        if not os.path.isfile(fullPath):
            self.regCode.msgBox("Error", f"File not found: {fullPath}")
            return

        try:
            if sys.platform.startswith('win'):
                os.startfile(fullPath)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', fullPath])
            else:  # Linux
                subprocess.Popen(['xdg-open', fullPath])
        except Exception as e:
            self.regCode.msgBox("Error", f"Cannot open file: {e}")

########################################################################################################################
    def showApplyScholarship(self, Id):
        from pageController import Controller
        self.controller = Controller()

        self.controller.showApplyScholarPage(Id)

########################################################################################################################
    def populateNotificationTbl(self, notiFilter):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/notifications/getNotificationData.php",
                data={
                    "email" : Sessions.seshEmail,
                    "filter" : notiFilter
                }
            )
            print(f"RAW RESPONSE: {response.text}")
            result = response.json()
            msg = result.get("message")

            if result.get("status") == "error":
                self.notificationsTableWidget.setRowCount(1)
                self.notificationsTableWidget.setColumnCount(1)
                self.notificationsTableWidget.setHorizontalHeaderLabels(["Message"])
                self.notificationsTableWidget.setItem(0, 0, QTableWidgetItem("You don't have any notifications."))
                return

            dbContent = result.get("data", [])


            self.notificationsTableWidget.setColumnCount(9)
            self.notificationsTableWidget.setRowCount(len(dbContent))
            self.notificationsTableWidget.setHorizontalHeaderLabels(
                [
                    "Actions",
                    "ID",
                    "title",
                    "msg",
                    "Sent From",
                    "Sent to",
                    "Status",
                    "Date Sent",
                    "Date Seen"
                ]

            )

            for rowIdx, rowData in enumerate(dbContent):
                self.notificationsTableWidget.setItem(rowIdx, 1, QTableWidgetItem(str(rowData.get("id")))),
                self.notificationsTableWidget.setItem(rowIdx, 2, QTableWidgetItem(rowData.get("title"))),
                self.notificationsTableWidget.setItem(rowIdx, 3, QTableWidgetItem(rowData.get("msg"))),
                self.notificationsTableWidget.setItem(rowIdx, 4, QTableWidgetItem(rowData.get("sender_name"))),
                self.notificationsTableWidget.setItem(rowIdx, 5, QTableWidgetItem(rowData.get("recipient_name"))),
                self.notificationsTableWidget.setItem(rowIdx, 6, QTableWidgetItem(rowData.get("noti_status"))),
                self.notificationsTableWidget.setItem(rowIdx, 7, QTableWidgetItem(rowData.get("date_sent"))),
                self.notificationsTableWidget.setItem(rowIdx, 8, QTableWidgetItem(str(rowData.get("date_seen") or "Not Seen")))

                #       create View & del btn
                viewBtn = QPushButton("View")
                # applyBtn = QPushButton("Apply")

                viewBtn.setStyleSheet("QPushButton { "
                                      "color: white;"
                                      "padding:3px;"
                                      "margin:0px;"
                                      "border-radius:3px;"
                                      "background-color:#010e1b;"
                                      "}")

                viewBtn.clicked.connect(
                    lambda _, Id=rowData.get("id"): self.showNotificationsDisplay(Id)
                )

                #   align horizontally
                btnWidget = QWidget()
                layout = QHBoxLayout(btnWidget)
                # layout.addWidget(applyBtn)
                layout.addWidget(viewBtn)
                layout.setContentsMargins(0, 0, 0, 0)

                #         add widget to tbl
                self.notificationsTableWidget.setCellWidget(rowIdx, 0, btnWidget)

            self.styleTbl(self.notificationsTableWidget)

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception Error(populateNotificationTbl): {e}"
            )
            print(f"Exception Error(populateNotificationTbl):{e}")

########################################################################################################################
    def styleTbl(self, tblWidget):
        tblWidget.setStyleSheet("QTableWidget { color: #010e1b; }")

        tblWidget.verticalHeader().setDefaultSectionSize(40)

        tblWidget.resizeColumnsToContents()

########################################################################################################################
    def showNotificationsDisplay(self, Id):
        from SholarshipManagementSystem.notificationsPage.notificationsDisplayCode import NotificationDisplay
        self.notiDisplay = NotificationDisplay(Id)
        self.notiDisplay.show()
