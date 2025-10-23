import json
import os
import subprocess
import sys
from datetime import datetime
import requests
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTableWidgetItem, QPushButton, QVBoxLayout, QMessageBox, \
    QLineEdit, QDialog, QLabel
from PyQt6.QtGui import QIcon
import Sessions
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from SholarshipManagementSystem.homePage.applicantDashboard import Ui_ApplicantDash
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.reportsPage.charts import Chart
from SholarshipManagementSystem.classes.applicant import Applicant
from SholarshipManagementSystem.reportsPage.report import Report

class ApplicantDash(QMainWindow, Ui_ApplicantDash):
    def __init__(self):
        super().__init__()
        self.login = None
        self.scheme = None
        self.charts = Chart()
        self.notiDisplay = None
        self.regCode = RegCode()
        self.controller = None
        self.reportPage = Report()
        self.applicant = Applicant(
            f"{Sessions.applicantName}",
            f"{Sessions.seshEmail}",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )
        self.setupUi(self)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))

        # DISPLAY HOME SCREEN
        self.mainDisplayWidget.setCurrentIndex(0)
        self.homeBtn.setChecked(True)
        self.homeIconBtn.setChecked(True)
        #HIDE SIDEBAR
        self.iconNameWidget.setVisible(False)

        #display username
        self.usernameLabel.setText(Sessions.applicantName)
        self.homeScreenUsernameLabel.setText(f"Hello {Sessions.applicantName}")

        #load plots
        self.loadPlot1()
        self.loadPlot2()
        self.loadPlot8()
        self.chartWidget.setFixedHeight(400)
        self.chart2Widget.setFixedHeight(400)
        self.mostCommonSchemesChart.setFixedHeight(400)

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

        self.printReportBtn.clicked.connect(self.printReport)

        #reportLogs
        self.reportLogsBtn.clicked.connect(self.switchToReportLogs)
        self.reportLogsIconBtn.clicked.connect(self.switchToReportLogs)

        #noti...
        self.notificationsBtn.clicked.connect(self.switchToNotifications)
        self.notificationsIconBtn.clicked.connect(self.switchToNotifications)
        #profile
        self.profileBtn.clicked.connect(self.switchToProfile)
        self.profileIconBtn.clicked.connect(self.switchToProfile)
        self.profileBtnQuickAccess.clicked.connect(self.switchToProfile)
        #------------------pass btn
        self.showPassBtn.clicked.connect(self.togglePasswordBtn)

        self.changeUsernameBtn.clicked.connect(self.changeUsername)
        self.changePassBtn.clicked.connect(self.changePassword)
        self.changeEmailBtn.clicked.connect(self.changeEmail)

        #logout
        self.logoutBtn.clicked.connect(self.logout)
        self.LogoutBtn.clicked.connect(self.logout)
        self.logoutIconBtn.clicked.connect(self.logout)

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
        self.populateCustomScholarships(Sessions.seshEmail)

    def switchToReports(self):
        self.mainDisplayWidget.setCurrentIndex(2)
        try:
            print("1")
            self.loadPlot3()
            print("2")
            self.loadPlot4()
            print("3")
            self.loadPlot5()
            print("4")
            self.loadPlot6()
            print("5")
            self.loadPlot7()

            self.schemesAvaliableTableWidget.setFixedHeight(300)
            self.populateSchemeTbl()
            self.populateCommonProgramTableWidget()
            self.schemeRatioChart.setFixedHeight(300)
            self.applicantEducationLevelChart.setFixedHeight(300)
            self.applicantsPerCountryChart.setFixedHeight(300)
            self.financialAmountPerScholarshipChart.setFixedHeight(300)

            #scholarship count
            self.totalNumOfScholarshipsLabelReports.setText(f"Total Number of Scholarships: {Sessions.scholarshipCount}")

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Something went wrong(reports): {e}"
            )
            print(f"Exception(reports){e}")

    def switchToReportLogs(self):
        self.mainDisplayWidget.setCurrentIndex(5)
        self.populateReportLogsTbl()


    def switchToNotifications(self):
        self.mainDisplayWidget.setCurrentIndex(3)
        self.populateNotificationTbl("All")

    def switchToProfile(self):
        self.mainDisplayWidget.setCurrentIndex(4)

########################################################################################################################
    def populateCustomScholarships(self, email):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/getCustomApplicantScholarships.php",
                data={
                    "email" : email
                }
            )

            print(f"RAW RESPONSE: {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown response")

            if result.get("status") == "success":
                self.customScholarshipLabel.setText("The scholarships displayed are based on your chosen program")
                dbContent = result.get("data", [])
                self.scholarshipTableWidget.setRowCount(
                    len(dbContent))  # always initialise tbl so it doesn't stack up rows
                Sessions.scholarshipCount = len(dbContent)

                self.scholarshipTableWidget.setColumnCount(12)

                self.scholarshipTableWidget.setHorizontalHeaderLabels(
                    [
                        "Actions",
                        "ID",
                        "Name",
                        "Descrip",
                        "Scheme",
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
                    self.scholarshipTableWidget.setItem(rowindx, 4, QTableWidgetItem(rowData.get("scheme_type", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 5, QTableWidgetItem(rowData.get("deadline", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 6,
                                                        QTableWidgetItem(rowData.get("financial_amount", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 7, QTableWidgetItem(rowData.get("provider", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 8, QTableWidgetItem(rowData.get("provider_email", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 9,
                                                        QTableWidgetItem(rowData.get("applicantion_link", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 10, QTableWidgetItem(
                        rowData.get("perks", "") or "No Benefits Available for this Scholarship"))
                    self.scholarshipTableWidget.setItem(rowindx, 11, QTableWidgetItem(rowData.get("file_path", "")))

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

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    "Error(populateCustomScholarships): There are currently no scholarships that match your program\nFeel free to explore the other scholarships"
                )
                self.customScholarshipLabel.setText("There are currently no scholarships that match your program\nFeel free to explore the other scholarships")
                print(f"Error(populateCustomScholarships): {msg}")

                self.populateScholarshipTbl()

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Something went wrong(populateCustomScholarships): {e}"
            )
            print(f"Exception(populateCustomScholarships){e}")

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

                self.scholarshipTableWidget.setColumnCount(12)

                self.scholarshipTableWidget.setHorizontalHeaderLabels(
                    [
                        "Actions",
                        "ID",
                        "Name",
                        "Descrip",
                        "Scheme",
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
                    self.scholarshipTableWidget.setItem(rowindx, 4, QTableWidgetItem(rowData.get("scheme_type", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 5, QTableWidgetItem(rowData.get("deadline", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 6,
                                                        QTableWidgetItem(rowData.get("financial_amount", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 7, QTableWidgetItem(rowData.get("provider", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 8, QTableWidgetItem(rowData.get("provider_email", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 9,
                                                        QTableWidgetItem(rowData.get("applicantion_link", "")))
                    self.scholarshipTableWidget.setItem(rowindx, 10, QTableWidgetItem(
                        rowData.get("perks", "") or "No Benefits Available for this Scholarship"))
                    self.scholarshipTableWidget.setItem(rowindx, 11, QTableWidgetItem(rowData.get("file_path", "")))

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
            self.regCode.msgBox(
                "Error",
                f"Something went wrong Populating scholarships tbl(dash): {e}"
            )
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

########################################################################################################################
    def plot1(self):
        self.chart1Label.setText("Scheme per Scholarship")
        return self.charts.barChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/schemeDataForChart.php",
            "Scholarships"
        )


    def loadPlot1(self):
        figure = FigureCanvas(self.plot1())
        layout = QVBoxLayout(self.chartWidget)
        layout.addWidget(figure)

########################################################################################################################
    def plot2(self):
        self.chart2Label.setText("Most Applied Scholarships")
        return self.charts.pieChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/mostAppliedScholarship.php"
        )

    def loadPlot2(self):
        figure = FigureCanvas(self.plot2())
        layout = QVBoxLayout(self.chart2Widget)
        layout.addWidget(figure)

########################################################################################################################
    def plot3(self):
        return self.charts.barChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/nationality.php",
            "Number of Applicants"
        )

    def loadPlot3(self):
        figure = FigureCanvas(self.plot3())
        layout = QVBoxLayout(self.applicantsPerCountryChart)
        layout.addWidget(figure)

########################################################################################################################
    def plot4(self):
        return self.charts.pieChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/educationLevel.php"
        )

    def loadPlot4(self):
        figure = FigureCanvas(self.plot4())
        layout = QVBoxLayout(self.applicantEducationLevelChart)
        layout.addWidget(figure)

########################################################################################################################
    def plot5(self):
        return self.charts.pieChart(
            "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/loadScholarshipCategories.php",
        )

    def loadPlot5(self):
        figure = FigureCanvas(self.plot5())
        layout = QVBoxLayout(self.financialAmountPerScholarshipChart)
        layout.addWidget(figure)

########################################################################################################################
    def plot6(self):
        return self.charts.pieChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/schemeDataForChart.php"
        )

    def loadPlot6(self):
        figure = FigureCanvas(self.plot6())
        layout = QVBoxLayout(self.schemeRatioChart)
        layout.addWidget(figure)

########################################################################################################################
    def plot7(self):
        return self.charts.barChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/mostAppliedScholarship.php",
            "Applications"
        )

    def loadPlot7(self):
        figure = FigureCanvas(self.plot7())
        layout = QVBoxLayout(self.mostAppliedScholarshipsChart)
        layout.addWidget(figure)

########################################################################################################################
    def plot8(self):
        return self.charts.barChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/nationality.php",
            "Number of Applicants"
        )

    def loadPlot8(self):
        figure = FigureCanvas(self.plot8())
        layout = QVBoxLayout(self.mostCommonSchemesChart)
        layout.addWidget(figure)

########################################################################################################################
    def populateCommonProgramTableWidget(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/applicant/getProgramForTbl.php"
            )
            print(f"RAW RESPONSE: {response.text}")
            result = response.json()

            if result.get("status") == "error":
                self.commonProgramsTableWidget.setRowCount(1)
                self.commonProgramsTableWidget.setColumnCount(1)
                self.commonProgramsTableWidget.setHorizontalHeaderLabels(["Message"])
                self.commonProgramsTableWidget.setItem(0, 0, QTableWidgetItem("NO INFORMATION TO DISPLAY"))
                return

            dbContent = result.get("data", [])

            self.commonProgramsTableWidget.setColumnCount(1)
            self.commonProgramsTableWidget.setRowCount(len(dbContent))
            self.commonProgramsTableWidget.setHorizontalHeaderLabels(
                [
                    "Program"
                ]

            )

            for rowIdx, rowData in enumerate(dbContent):
                self.commonProgramsTableWidget.setItem(rowIdx, 0, QTableWidgetItem(rowData.get("program")))

            self.styleTbl(self.commonProgramsTableWidget)

        except Exception as e:
            self.regCode.msgBox("Error", f"Exception: {e}")

########################################################################################################################
    def populateSchemeTbl(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/chartData/schemeDataForTbl.php"
            )
            print(f"RAW RESPONSE: {response.text}")
            result = response.json()

            if result.get("status") == "error":
                self.schemesAvaliableTableWidget.setRowCount(1)
                self.schemesAvaliableTableWidget.setColumnCount(1)
                self.schemesAvaliableTableWidget.setHorizontalHeaderLabels(["Message"])
                self.schemesAvaliableTableWidget.setItem(0, 0, QTableWidgetItem("NO INFORMATION TO DISPLAY"))
                return

            dbContent = result.get("data", [])

            self.schemesAvaliableTableWidget.setColumnCount(5)
            self.schemesAvaliableTableWidget.setRowCount(len(dbContent))
            self.schemesAvaliableTableWidget.setHorizontalHeaderLabels(
                [
                    "Actions",
                    "ID",
                    "Scheme",
                    "Description",
                    "Benefit Details"
                ]

            )

            for rowIdx, rowData in enumerate(dbContent):
                self.schemesAvaliableTableWidget.setItem(rowIdx, 1, QTableWidgetItem(str(rowData.get("id"))))
                self.schemesAvaliableTableWidget.setItem(rowIdx, 2, QTableWidgetItem(rowData.get("scheme_name")))
                self.schemesAvaliableTableWidget.setItem(rowIdx, 3, QTableWidgetItem(rowData.get("description")))
                self.schemesAvaliableTableWidget.setItem(rowIdx, 4, QTableWidgetItem(rowData.get("benefit_details")))

                #       create View & del btn
                viewBtn = QPushButton("View")

                viewBtn.setStyleSheet("QPushButton { "
                                      "color: white;"
                                      "background-color: #010e1b;"
                                      "padding:3px;"
                                      "margin:0px;"
                                      "border-radius:3px;"
                                      "}")

                viewBtn.clicked.connect(
                    lambda _, Id=rowData.get("id"): self.displayScheme(Id)
                )
                #   align horizontally
                btnWidget = QWidget()
                layout = QHBoxLayout(btnWidget)
                layout.addWidget(viewBtn)
                layout.setContentsMargins(0, 0, 0, 0)

                #         add widget to tbl
                self.schemesAvaliableTableWidget.setCellWidget(rowIdx, 0, btnWidget)

            self.styleTbl(self.schemesAvaliableTableWidget)

        except Exception as e:
            self.regCode.msgBox("Error", f"Exception(populateSchemeTbl): {e}")
            print(f"Exception(populateSchemeTbl): {e}")
########################################################################################################################
    def displayScheme(self,Id):
        from SholarshipManagementSystem.schemes.schemeDisplayCode import SchemeDetails
        self.scheme = SchemeDetails(Id)
        self.scheme.show()

########################################################################################################################
    def changeUsername(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to change Username"):
            result = self.applicant.updateDetails(
                "username",
                f"{self.usernameTxt.text().strip()}"
            )
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Process Failed",
                    msg
                )
        else:
            pass

########################################################################################################################
    def changeEmail(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to change Email"):
            result = self.applicant.updateDetails(
                "email",
                f"{self.emailTxt.text().strip()}"
            )
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Process Failed",
                    msg
                )
        else:
            pass

########################################################################################################################
    def changePassword(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to change Password"):
            result = self.applicant.updateDetails(
                "pass",
                f"{self.passTxt.text().strip()}"
            )
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Process Failed",
                    msg
                )
        else:
            pass
########################################################################################################################
    def logout(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to Logout?"):
            from pageController import Controller
            controller = Controller()
            controller.showLogin()
            self.close()
        else:
            pass

########################################################################################################################
    def confirmMsgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        result = msgBox.exec()

        if result == QMessageBox.StandardButton.Ok:
            return True
        else:
            return False

    ########################################################################################################################
    def togglePasswordBtn(self):
        if self.passTxt.echoMode() == QLineEdit.EchoMode.Normal:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Password)
            self.showPassBtn.setIcon(QIcon(":icons/seeWhiteIcon.png"))
        else:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.showPassBtn.setIcon(QIcon(":icons/hideWhite.png"))

    def printReport(self):
        try:
            # Create dialog
            dialog = QDialog()
            dialog.setWindowTitle("YOUR REPORT IS READY")

            layout = QVBoxLayout()
            hbox = QHBoxLayout()

            heading = QLabel("REPORT GENERATION")

            label = QLabel("Report Name:")
            hbox.addWidget(label)

            # Create QLineEdit with default filename
            current_date = datetime.now().strftime("%Y-%m-%d")
            base_name = f"report_{current_date}"
            report_dir = "C:/Users/Yankho/OneDrive/Desktop/PROJECT/reportLogs/applicantReports"
            os.makedirs(report_dir, exist_ok=True)

            # Find next number in sequence
            existing = [f for f in os.listdir(report_dir) if f.startswith(base_name)]
            report_number = len(existing) + 1
            default_name = f"{base_name}_{report_number}"

            reportTxt = QLineEdit(default_name)
            hbox.addWidget(reportTxt)
            layout.addWidget(heading)
            layout.addLayout(hbox)

            # OK and Cancel buttons
            btnSave = QPushButton("Generate Report")
            btnCancel = QPushButton("Cancel")
            layout.addWidget(btnSave)
            layout.addWidget(btnCancel)

            dialog.setLayout(layout)

            # Button clicks
            btnCancel.clicked.connect(dialog.reject)
            btnSave.clicked.connect(dialog.accept)

            # Execute dialog
            if dialog.exec():
                report_name = reportTxt.text().strip()
                if not report_name:
                    QMessageBox.warning(self, "Error", "Please enter a report name.")
                    return

                self.reportPage.generateReportForApplicant(self.scrollArea_2, report_name)
                QMessageBox.information(self, "Success", f"Report '{report_name}' has been generated.")
                demoDir = f"{report_dir}/{report_name}.pdf"

                print(demoDir)

                self.reportPage.insertReport(
                    report_name,
                    demoDir,
                    Sessions.seshEmail,
                    "applicant"
                )

        except Exception as e:
            self.regCode.msgBox("Error", f"Exception(printReportApplicant): {e}")
            print(f"Exception(printReportApplicant):{e}")

########################################################################################################################
    def populateReportLogsTbl(self):
         msg = self.reportPage.populateReportLogs(
            "applicant",
            self.reportLogsTableWidget,
            Sessions.seshEmail,
            self.pdfViewerScrollWidget.widget()
        )
         self.reportMsgLabel.setText(msg)