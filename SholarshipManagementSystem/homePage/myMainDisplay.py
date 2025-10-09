import json
import os
import subprocess
import sys
import requests
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, \
    QVBoxLayout, QCompleter,QLabel
from SholarshipManagementSystem.homePage.dashboard import Ui_MainWindow
import Sessions
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from SholarshipManagementSystem.manageApplicantl.applicantCardCode import ApplicantCard
from SholarshipManagementSystem.reportsPage.charts import Chart
from SholarshipManagementSystem.classes.admin import Admin


class Dash(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.appDetails = None
        self.admin = Admin(Sessions.adminName, Sessions.seshEmail, "*********")
        self.charts = Chart()
        self.setupUi(self)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))

        #DISPLAY HOME SCREEN
        self.mainDisplayWidget.setCurrentIndex(0)
        self.populateApplicantTbl()
        self.populateTableWidget()
        self.homeBtn.click()
        self.homeIconBtn.click()
        self.totalNumberOfApplicantsLabelHome.setText(f"Total Number Of Applicants: {Sessions.applicantCount}")
        self.totalNumberOfApplicantsLabelReports.setText(f"Total Number Of Applicants: {Sessions.applicantCount}")

        self.totalNumOfScholarshipsLabelReports.setText(f"Total Number Scholarships: {Sessions.scholarshipCount}")
        self.totalNumOfScholarshipsLabelHome.setText(f"Total Number Scholarships: {Sessions.scholarshipCount}")

        #HIDE SIDEBAR
        self.iconNameWidget.setHidden(True)

        # DISPLAY USERNAME
        self.usernameLabel.setText(Sessions.adminName)
        self.homeScreenUsernameLabel.setText(f"Hello {Sessions.adminName}")

        #BTN CLICKS
        self.BtnClicks()

        #preriquisutes

        self.loadPlot()
        self.loadPlot2()
        #index to load different charts
        self.idx = 1
        #chart labels
        self.chart1Label.setText("Applicant Education Level")
        self.chart2Label.setText("Applicant per country")

        self.listofApplicantsTableWidget.setFixedHeight(300)
        self.chartWidget.setFixedHeight(300)
        self.chart2Widget.setFixedHeight(300)

    ####BTN CLICKS#########################################################################################################
    def BtnClicks(self):
        # Home
        self.homeBtn.clicked.connect(self.switchToDash)
        self.homeIconBtn.clicked.connect(self.switchToDash)
        # scholar...
        self.scholarshipBtn.clicked.connect(self.switchToScholarshipPage)
        self.scholarshipIconBtn.clicked.connect(self.switchToScholarshipPage)
        self.uploadScholarshipBtn.clicked.connect(self.showUploadScholarship)
        # report
        self.reportBtn.clicked.connect(self.switchToReportsPage)
        self.reportIconBtn.clicked.connect(self.switchToReportsPage)
        #manageApplicant
        self.manageApplicantBtn.clicked.connect(self.switchToManageApplicants)
        self.manageApplicantIconBtn.clicked.connect(self.switchToManageApplicants)
        # profile
        self.profileBtn.clicked.connect(self.switchToProfilePage)
        self.profileIconBtn.clicked.connect(self.switchToProfilePage)
        self.profileBtnQuickAccess.clicked.connect(self.switchToProfilePage)
        # noti...
        self.notificationsBtn.clicked.connect(self.switchToNotificationsPage)
        self.notificationsIconBtn.clicked.connect(self.switchToNotificationsPage)
        #     show password
        self.showPassBtn.clicked.connect(self.togglePasswordBtn)

        #     sendNotification
        self.sendNotificationsBtn.clicked.connect(self.sendNotification)

        #     filterBtn(applicant)
        self.filterBtn.clicked.connect(
            lambda: self.populateApplicantPerSubject(
                "http://localhost/BackEnd/scholarshipManagement/applicant/filteredApplicant.php",
                f"{self.subjectFilterCombo.currentText().strip()}"
            )
        )
        #     filter btn(scholarship)
        self.scholarshipFilterBtn.clicked.connect(
            lambda: self.populateScholarshipTbl(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/filteredScholarships.php",
                self.subjectScholarshipFilterCombo.currentText().strip()
            )
        )

        #     LOGOUT
        self.logoutBtn.clicked.connect(self.logout)
        self.LogoutBtn.clicked.connect(self.logout)
        self.logoutIconBtn.clicked.connect(self.logout)

        #     update details BTNS
        self.changeEmailBtn.clicked.connect(self.changeEmail)
        self.changeUsernameTxt.clicked.connect(self.changeUsername)
        self.changePassBtn.clicked.connect(self.changePass)

        #changeCharts btn
        self.changeChartBtn.clicked.connect(self.loadRandChart)

    ###PASSWORD#########################################################################################################
    def togglePasswordBtn(self):
        if self.passTxt.echoMode() == QLineEdit.EchoMode.Normal:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Password)
            self.showPassBtn.setIcon(QIcon(":icons/seeWhiteIcon.png"))
        else:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.showPassBtn.setIcon(QIcon(":icons/hideWhite.png"))

########################################################################################################################
    def getAdminDetails(self):
        self.usernameTxt.setText(Sessions.adminName)
        self.emailTxt.setText(Sessions.seshEmail)
        # self.passTxt.setText("RANDOM PASSWORD")

########################################################################################################################
    def maximisePage(self):
        QTimer.singleShot(0, self.showMaximized)

# PAGE SWITCHING####################################################################################################
    def switchToDash(self):
        self.mainDisplayWidget.setCurrentIndex(0)

    def switchToScholarshipPage(self):
        self.mainDisplayWidget.setCurrentIndex(1)
        #     POPULATE TBL
        self.populateTableWidget()

    def switchToNotificationsPage(self):
        self.mainDisplayWidget.setCurrentIndex(4)
        self.populateApplicantEmailLineEdit()

    def switchToProfilePage(self):
        self.mainDisplayWidget.setCurrentIndex(5)
        #set dateJoined
        self.getAdminDetails()
        try:
            data = self.admin.getAdminDetails()
            adminData = data.get("data", [])
            self.dateJoinedLabel.setText(
                f"Date Joined: {adminData[0]["date_joined"]}"
            )
        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception Error(adminData_Dash): {e}"
            )

    def switchToReportsPage(self):
        try:
            self.populateApplicantRankTbl()
            print("CHECKPOINT 1")
            self.mainDisplayWidget.setCurrentIndex(3)
            print("CHECKPOINT 2")
            self.loadPlot3()
            print("CHECKPOINT 3")
            self.loadPlot4()
            print("CHECKPOINT 4")
            self.loadPlot5()
            print("CHECKPOINT 4")
            self.applicantsThisWeekChart.setFixedHeight(300)
            self.applicantsPerCountryChart.setFixedHeight(300)
            self.applicantPerSubjectTableWidget.setFixedHeight(300)
            self.scholarshipPerSubjectTableWidget.setFixedHeight(300)
            self.applicantRankTableWidget.setFixedHeight(300)
            print("CHECKPOINT 5")
            self.populateApplicantFilter()
            self.populateScholarshipFilter()
            print("CHECKPOINT 6")
            self.populateApplicantPerSubject(
                "http://localhost/BackEnd/scholarshipManagement/applicant/filteredApplicant.php",
                "All"
            )

            self.populateScholarshipTbl(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/filteredScholarships.php",
                "All"
            )
        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception: {e}"
            )
            print(f"Exception: {e}")

    def switchToManageApplicants(self):
        self.mainDisplayWidget.setCurrentIndex(2)
        self.showManageApplicantPage()

# PAGE SWITCHING END################################################################################################

# POPULATE TABLE WIDGET#############################################################################################
    def populateTableWidget(self):

        print(f"Admin Email: {Sessions.seshEmail}")
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/getScholarshipDetails.php")

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
                    delBtn = QPushButton("Delete")

                    viewBtn.setStyleSheet("QPushButton { "
                                          "color: white;"
                                          "padding:3px;"
                                          "margin:0px;"
                                          "border-radius:3px;"
                                          "}")
                    delBtn.setStyleSheet("QPushButton { "
                                         "color: white;"
                                         "padding:3px;"
                                         "margin:0px;"
                                         "border-radius:3px;"
                                         "}")

                    viewBtn.clicked.connect(
                        lambda _, path=rowData.get("file_path"): self.displayScholarshipDoc(path)
                    )
                    delBtn.clicked.connect(
                        lambda _, Id=rowData.get("id"): self.delScholarship(Id)
                    )
                    #   align horizontally
                    btnWidget = QWidget()
                    layout = QHBoxLayout(btnWidget)
                    layout.addWidget(viewBtn)
                    layout.addWidget(delBtn)
                    layout.setContentsMargins(0, 0, 0, 0)

                    #         add widget to tbl
                    self.scholarshipTableWidget.setCellWidget(rowindx, 0, btnWidget)

                self.styleTbl()



            elif result.get("message") == "error":
                self.msgBox("Error(ScholarTbl)", f"Error: {msg}")
                print(msg)

        except Exception as e:
            self.msgBox("Error", f"Something went wrong Populating scholarships tbl(dash): {e}")
            print(e)

### DISPLAY SCHOLARSHIPS########################################################################################
    def displayScholarshipDoc(self, path):

        print(repr(path))
        # referenceDir = "C:/XAMPP/htdocs/BackEnd/scholarshipManagement/uploadScholarships/docs/uploadedFiles"
        xamppDir = r"C:/XAMPP/htdocs/BackEnd/scholarshipManagement/uploadScholarships/docs/uploadedFiles"

        fullPath = os.path.join(xamppDir, path)

        fullPath = os.path.normpath(fullPath)

        print(fullPath)
        os.startfile(fullPath)

        if not os.path.isfile(fullPath):
            self.msgBox("Error", f"File not found: {fullPath}")
            return

        try:
            if sys.platform.startswith('win'):
                os.startfile(fullPath)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', fullPath])
            else:  # Linux
                subprocess.Popen(['xdg-open', fullPath])
        except Exception as e:
            self.msgBox("Error", f"Cannot open file: {e}")

####### DELETE SCHOLARSHIPS#############################################################################################
    def delScholarship(self, Id):
        print(f"id: {Id}")

        try:

            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/deleteScholarship.php",
                data={
                    "id": Id
                }
            )

            result = json.loads(response.text)
            msg = result.get("message")

            if result.get("status") == "success":
                self.populateTableWidget()
                self.msgBox("Process Complete", f"{msg}")
                print(f"Delete successful: {msg}")

            elif result.get("status") == "error":
                self.msgBox("delete failed(dash)", f": {msg}")
                print(f"deleting(dash): {msg}")



        except Exception as e:
            self.msgBox("Error", f"Something went wrong while deleting(dash): {e}")
            print(f"deleting(dash): {e}")

########################################################################################################################
    def showUploadScholarship(self):
        from pageController import Controller
        self.controller = Controller()
        self.controller.showUploadScholarship()

####TABLE STYLESHEET####################################################################################################
    def styleTbl(self):
        self.scholarshipTableWidget.setStyleSheet("QTableWidget { color: #010e1b; }")

        self.scholarshipTableWidget.verticalHeader().setDefaultSectionSize(40)

        self.scholarshipTableWidget.resizeColumnsToContents()

        # self.scholarshipTableWidget.horizontalHeader().setStretchLastSection(True)

        # btn size adjustment
        # for row in range(self.scholarshipTableWidget.rowCount()):
        #     cellWidget = self.scholarshipTableWidget.cellWidget(row, 5)
        #     if cellWidget:
        #         for i in range(cellWidget.layout().count()):
        #             btn = cellWidget.layout().itemAt(i).widget()
        #             btn.setMinimumWidth(60)
        #             btn.setMaximumHeight(25)

########################################################################################################################
    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

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
    def plot1(self):

        return self.charts.pieChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/educationLevel.php"
        )

    def loadPlot(self):
        figure = FigureCanvas(self.plot1())
        layout = QVBoxLayout(self.chartWidget)
        layout.addWidget(figure)

########################################################################################################################
    def plot2(self):
        return self.charts.barChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/nationality.php",
            "Number of Applicants"
        )

    def loadPlot2(self):
        figure = FigureCanvas(self.plot2())
        layout = QVBoxLayout(self.chart2Widget)
        layout.addWidget(figure)

########################################################################################################################
    def plot3(self):

        return self.charts.pieChart(
            "http://localhost/BackEnd/scholarshipManagement/chartData/nationality.php"
        )

    def loadPlot3(self):
        figure = FigureCanvas(self.plot3())
        layout = QVBoxLayout(self.applicantsPerCountryChart)
        layout.addWidget(figure)

########################################################################################################################
    def plot4(self):
        title = "Applicants Registered this week"

        return self.charts.lineGraph(
            "http://localhost/BackEnd/scholarshipManagement/applicant/applicantsRegisteredPerWeek.php",
            "Number of applicants"
        )

    def loadPlot4(self):
        figure = FigureCanvas(self.plot4())
        layout = QVBoxLayout(self.applicantsThisWeekChart)
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
    def loadHomePageCharts1(self):
        try:
            self.clearLayout(self.chartWidget)
            self.clearLayout(self.chart2Widget)

            self.chart1Label.setText("Applicant Education Level")
            figure = FigureCanvas(self.plot1())
            layout = QVBoxLayout(self.chartWidget)
            layout.addWidget(figure)
            self.chartWidget.setLayout(layout)

            self.chart2Label.setText("Applicant per country")
            figure2 = FigureCanvas(self.plot2())
            layout2 = QVBoxLayout(self.chart2Widget)
            layout2.addWidget(figure2)
            self.chart2Widget.setLayout(layout2)

        except Exception as e:
            print(f"Exception(loadHomePageCharts1): {e}")

########################################################################################################################
    def loadHomePageCharts2(self):
        try:
            self.clearLayout(self.chartWidget)
            self.clearLayout(self.chart2Widget)

            self.chart1Label.setText("Applications this week")
            figure = FigureCanvas(self.plot4())
            layout = QVBoxLayout(self.chartWidget)
            layout.addWidget(figure)
            self.chartWidget.setLayout(layout)

            self.chart2Label.setText("Financial benefit per scholarship")
            figure2 = FigureCanvas(self.plot5())
            layout2 = QVBoxLayout(self.chart2Widget)
            layout2.addWidget(figure2)
            self.chart2Widget.setLayout(layout2)

        except Exception as e:
            print(f"Exception(loadHomePageCharts2): {e}")

########################################################################################################################
    def clearLayout(self, widget):

        layout = widget.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            QWidget().setLayout(layout)

########################################################################################################################
    def loadRandChart(self):
        self.homePageCharts = [
            self.loadHomePageCharts1,
            self.loadHomePageCharts2
        ]

        chartFunction = self.homePageCharts[self.idx]
        chartFunction()

        self.idx = (self.idx + 1) % len(self.homePageCharts)


########################################################################################################################
    def populateApplicantTbl(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/applicant/loadApplicantData.php"
            )

            print(F"RAW RESPONSE: {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown response")

            if result.get("status") == "success":
                #     get db content
                dbContent = result.get("data", [])
                # Sessions.seshEmail
                print(dbContent)
                self.listofApplicantsTableWidget.setRowCount(
                    len(dbContent))  # always initialise tbl so it doesn't stack up rows
                Sessions.applicantCount = len(dbContent)

                self.listofApplicantsTableWidget.setColumnCount(10)

                self.listofApplicantsTableWidget.setHorizontalHeaderLabels(
                    [
                        "Actions",
                        "ID",
                        "Name",
                        "Email",
                        "Age",
                        "Gender",
                        "Nationality",
                        "Education Level",
                        "DOB",
                        "Overall Score"
                    ]
                )

                #     populate tbl with content from db
                for rowindx, rowData in enumerate(dbContent):
                    #         fill data for all 4 columns
                    self.listofApplicantsTableWidget.setItem(rowindx, 1, QTableWidgetItem(str(rowData.get("id", ""))))
                    self.listofApplicantsTableWidget.setItem(rowindx, 2, QTableWidgetItem(rowData.get("name", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 3, QTableWidgetItem(rowData.get("email", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 4, QTableWidgetItem(
                        str(rowData.get("age", "")) or "Not specified"))
                    self.listofApplicantsTableWidget.setItem(rowindx, 5, QTableWidgetItem(
                        rowData.get("gender", "") or "Not specified"))
                    self.listofApplicantsTableWidget.setItem(rowindx, 6, QTableWidgetItem(
                        rowData.get("nationality", "") or "Not specified"))
                    self.listofApplicantsTableWidget.setItem(rowindx, 7,
                                                             QTableWidgetItem(rowData.get("education_level", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 8, QTableWidgetItem(rowData.get("dob", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 9,
                                                             QTableWidgetItem(str(rowData.get("score", "")) or 0))

                    #       create View & del btn
                    viewBtn = QPushButton("View")
                    delBtn = QPushButton("Delete")

                    viewBtn.setStyleSheet("QPushButton { "
                                          "color: white;"
                                          "padding:3px;"
                                          "margin:0px;"
                                          "border-radius:3px;"
                                          "}")
                    delBtn.setStyleSheet("QPushButton { "
                                         "color: white;"
                                         "padding:3px;"
                                         "margin:0px;"
                                         "border-radius:3px;"
                                         "}")

                    viewBtn.clicked.connect(
                        lambda _, Id=rowData.get("id"): self.displayApplicantDetails(Id)
                    )
                    delBtn.clicked.connect(
                        lambda _, Id=rowData.get("id"): self.delApplicant(Id)
                    )
                    #   align horizontally
                    btnWidget = QWidget()
                    layout = QHBoxLayout(btnWidget)
                    layout.addWidget(viewBtn)
                    layout.addWidget(delBtn)
                    layout.setContentsMargins(0, 0, 0, 0)

                    #         add widget to tbl
                    self.listofApplicantsTableWidget.setCellWidget(rowindx, 0, btnWidget)

                    self.listofApplicantsTableWidget.setStyleSheet("QTableWidget { color: #010e1b; }")

                    self.listofApplicantsTableWidget.verticalHeader().setDefaultSectionSize(40)

                    self.listofApplicantsTableWidget.resizeColumnsToContents()


            elif result.get("message") == "error":
                self.msgBox("Error(upload)", f"Upload error: {msg}")
                print(msg)

        except Exception as e:
            self.msgBox("Error", f"Something went wrong Populating Applicant tbl(dash): {e}")
            print(e)

########################################################################################################################
    def delApplicant(self, Id):
        print(f"id: {Id}")

        try:

            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/applicant/deleteApplicant.php",
                data={
                    "id": Id
                }
            )

            result = json.loads(response.text)
            msg = result.get("message")

            if result.get("status") == "success":
                self.msgBox("Process Complete", f"{msg}")
                print(f"Delete successful: {msg}")
                self.populateApplicantTbl()

            elif result.get("status") == "error":
                self.msgBox("delete failed(dash)", f"{msg}")
                print(f"deleting(dash): {msg}")
        except Exception as e:
            self.msgBox("Error", f"Something went wrong while Deleting Applicant(dash): {e}")
            print(e)

########################################################################################################################
    def populateApplicantEmailLineEdit(self):
        # msg population
        quickTitle = [
            "Application Accepted.",
            "Application Denied",
            "Account Verification"
        ]

        completer = QCompleter(quickTitle, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)  # live filter anywhere in the string
        completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

        self.notificationTitleTxt.setCompleter(completer)

        #msg population
        quickMsg = [
            "Congratulations, You have been accepted!",
            "We are sorry to inform you that you have NOT been accepted. Please feel free to Apply for the next scholarship",
            "Your account is not verified. Please get it verified before you are removed from the system!"
        ]

        completer = QCompleter(quickMsg, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)  # live filter anywhere in the string
        completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

        self.notificationMsgTxt.setCompleter(completer)

        # email populations
        self.notificationEmailTxt.setPlaceholderText("user@gmail.com")

        url = "http://localhost/BackEnd/scholarshipManagement/applicant/getApplicantEmails.php"

        try:
            response = requests.get(url)
            result = response.json()
            msg = result.get("message", "Unknown Msg")

            if result["status"] == "error":
                self.msgBox(
                    "Error(LiveFiltering)",
                    f"Something went wrong:\n{msg}"
                )
                print(f"Something went wrong(LiveFiltering):\n{msg}")
                return

            elif result["status"] == "success":
                dbEmails = result["data"]

                completer = QCompleter(dbEmails, self)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                completer.setFilterMode(Qt.MatchFlag.MatchContains)  # live filter anywhere in the string
                completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

                self.notificationEmailTxt.setCompleter(completer)

        except Exception as e:
            self.msgBox(
                "Error(LiveFiltering)",
                f"Exception Error:\n{e}"
            )
            print(f"Exception Error:\n{e}")
            return

########################################################################################################################
    def displayApplicantDetails(self, Id):
        from SholarshipManagementSystem.homePage.applicantDetailsCode import ApplicantDetails
        self.appDetails = ApplicantDetails(Id)
        self.appDetails.show()

########################################################################################################################
    def populateApplicantRankTbl(self):
        url = "http://localhost/BackEnd/scholarshipManagement/applicant/applicantRank.php"

        try:
            response = requests.get(url)
            result = response.json()
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.msgBox(
                    "Error",
                    f"Something went wrong: {msg}"
                )
                return

            print(f"RAW RESPONSE: {response.text}")

            dbContent = result.get("data", [])

            self.applicantRankTableWidget.setRowCount(len(dbContent))
            self.applicantRankTableWidget.setColumnCount(2)

            self.applicantRankTableWidget.setHorizontalHeaderLabels(
                [
                    "Name",
                    "Score"
                ]
            )

            for rowindx, rowData in enumerate(dbContent):
                self.applicantRankTableWidget.setItem(rowindx, 0,
                                                      QTableWidgetItem(rowData.get("name", "Display Error")))
                self.applicantRankTableWidget.setItem(rowindx, 1,
                                                      QTableWidgetItem(str(rowData.get("score", "Display Error"))))

            # self.applicantRankTableWidget.resizeColumnsToContents()
        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception: {e}")

########################################################################################################################
    def populateApplicantPerSubject(self, url, selectedFilter):
        try:
            response = requests.post(
                url,
                data={
                    "filter": selectedFilter
                }
            )
            result = response.json()
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.msgBox(
                    "Error",
                    f"Something went wrong: {msg}"
                )
                return

            print(f"RAW RESPONSE: {response.text}")

            dbContent = result.get("data", [])

            self.applicantPerSubjectTableWidget.setRowCount(len(dbContent))
            self.applicantPerSubjectTableWidget.setColumnCount(2)

            self.applicantPerSubjectTableWidget.setHorizontalHeaderLabels(
                [
                    "Scholarship Name",
                    "Subject"
                ]
            )

            for rowindx, rowData in enumerate(dbContent):
                self.applicantPerSubjectTableWidget.setItem(rowindx, 0, QTableWidgetItem(rowData["name"]))
                self.applicantPerSubjectTableWidget.setItem(rowindx, 1, QTableWidgetItem(str(rowData.get("subject", "Display Error"))))

        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception(Reports): {e}")
            print(f"Exception(Reports): {e}")

########################################################################################################################
    def populateApplicantFilter(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/applicant/getSubject.php"
            )

            result = response.json()
            print(f"RAW RESPONSE : {response.text}")

            msg = result.get("message")

            if result.get("status") == "error":
                self.msgBox(
                    "Error",
                    f"{msg}")
                print(f"Error: {msg}")
                return

            dbContent = result.get("data", [])

            self.subjectFilterCombo.addItem("All")
            self.subjectFilterCombo.addItems(dbContent)

        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception(filterCombo): {e}")
            print(f"Exception(filterCombo): {e}")

########################################################################################################################
    def populateScholarshipTbl(self, url, selectedFilter):

        try:
            response = requests.post(
                url,
                data={
                    "filter": selectedFilter
                }
            )

            result = response.json()
            print(f"RAW RESPONSE: {response.text}")

            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.msgBox(
                    "Error",
                    f"{msg}")
                print(f"Error: {msg}")
                return

            dbContent = result.get("data", [])

            self.scholarshipPerSubjectTableWidget.setColumnCount(2)
            self.scholarshipPerSubjectTableWidget.setRowCount(len(dbContent))

            self.scholarshipPerSubjectTableWidget.setHorizontalHeaderLabels(
                [
                    "Name",
                    "Subject"
                ]
            )

            for rowindx, rowData in enumerate(dbContent):
                self.scholarshipPerSubjectTableWidget.setItem(rowindx, 0,
                                                              QTableWidgetItem(rowData.get("name", "Display Error")))
                self.scholarshipPerSubjectTableWidget.setItem(rowindx, 1, QTableWidgetItem(
                    str(rowData.get("subject", "Display Error"))))
        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception(scholarshipTbl): {e}")
            print(f"Exception(scholarshipTbl): {e}")

########################################################################################################################
    def populateScholarshipFilter(self):

        url = "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/getSubject.php"
        try:
            response = requests.get(url)

            result = response.json()
            print(f"RAW RESPONSE : {response.text}")

            msg = result.get("message")

            if result.get("status") == "error":
                self.msgBox(
                    "Error",
                    f"{msg}")
                print(f"Error: {msg}")
                return

            dbContent = result.get("data", [])

            self.subjectScholarshipFilterCombo.addItem("All")
            self.subjectScholarshipFilterCombo.addItems(dbContent)
        except Exception as e:
            self.msgBox(
                "Error",
                f"Exception(scholarshipFilter): {e}")
            print(f"Exception(scholarshipFilter): {e}")


########################################################################################################################
    def sendNotification(self):
        result = self.admin.sendNotification(
            self.notificationEmailTxt,
            self.notificationTitleTxt,
            self.notificationMsgTxt
        )

        msg = result.get("message", "Unknown Msg")

        if result.get("status") == "success":
            self.msgBox(
                "Email sent",
                msg
            )
        elif result.get("status") == "error":
            self.msgBox(
                "Error",
                msg
            )

########################################################################################################################
    def changePass(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to continue"):
            result = self.admin.updateDetails(
                "pass",
                f"{self.passTxt.text().strip()}"
            )

            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "success":
                self.msgBox(
                    "Process Complete",
                    msg
                )

            elif result.get("status") == "error":
                self.msgBox(
                    "Process Failed",
                    msg
                )
        else:
            pass

########################################################################################################################
    def changeEmail(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to continue"):
            result = self.admin.updateDetails(
                "email",
                f"{self.emailTxt.text().strip()}"
            )

            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "success":
                self.msgBox(
                    "Process Complete",
                    msg
                )

            elif result.get("status") == "error":
                self.msgBox(
                    "Process Failed",
                    msg
                )
        else:
            pass

########################################################################################################################
    def changeUsername(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to continue"):
            result = self.admin.updateDetails(
                "username",
                f"{self.usernameTxt.text().strip()}"
            )
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "success":
                self.msgBox(
                    "Process Complete",
                    msg
                )

            elif result.get("status") == "error":
                self.msgBox(
                    "Process Failed",
                    msg
                )
        else:
            pass

########################################################################################################################
    def logout(self):
        if self.confirmMsgBox("Confirm Action", "Do you want to continue"):
            from pageController import Controller
            controller = Controller()
            controller.showLogin()
            self.close()
        else:
            pass

########################################################################################################################
    def showManageApplicantPage(self):

        try:

            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/applicant/loadApplicantData.php"
            )
            result = response.json()
            if result.get("status") == "error":
                self.msgBox("Error", result.get("message", "Unknown error"))
                return
            # print("CHECKPOINT 1")
            dbContent = result.get("data", [])

            self.manageApplicantScroll.setWidgetResizable(True)

            # clear any previous content
            old = self.manageApplicantScroll.takeWidget()
            if old:
                old.deleteLater()
            # print("CHECKPOINT 2")
            #new content
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(12)
            # print("CHECKPOINT 3")
            # Page title
            pageTitle = QLabel("MANAGE APPLICANT")
            pageTitle.setStyleSheet("font: 700 16pt 'Segoe UI';")
            pageTitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addWidget(pageTitle)
            # print("CHECKPOINT 3")
            # Search bar
            searchLayout = QHBoxLayout()
            searchBar = QLineEdit()
            searchBar.setStyleSheet("""
            width:300px;
            padding:7px;
            """)
            searchBar.setPlaceholderText("Type name or email")
            # print("CHECKPOINT 4")
            #search btn
            searchBtn = QPushButton()
            searchBtn.setIcon(QIcon(":/icons/search.png"))
            searchBtn.setStyleSheet("""
            padding:7px;
            margin:0px;
            background: #063970;
            """)
            # print("CHECKPOINT 5")
            searchLayout.addStretch(1)
            searchLayout.addWidget(searchBar)
            searchLayout.addWidget(searchBtn)
            searchLayout.addStretch(1)
            layout.addLayout(searchLayout)
            # print("CHECKPOINT 6")

            # Applicant cards
            for d in dbContent:
                card = ApplicantCard(d.get("name"), d.get("email"))
                # Make each card highlight on hover
                card.setStyleSheet("""
                    QWidget {
                        padding: 8px;
                        background: #063970;
                    }
                    QWidget::hover {
                        color:black;
                    }
                """)
                layout.addWidget(card)
                # print("CHECKPOINT 7")

            # Add a stretch at the bottom so cards stay at the top
            layout.addStretch(1)

            # Put this container into the designer scroll area
            self.manageApplicantScroll.setWidget(container)

            #set the current index, no insertWidget needed.
            self.mainDisplayWidget.setCurrentIndex(2)
            # print("CHECKPOINT 8")

        except Exception as e:
            self.msgBox("Error", f"Exception: {e}")
            print(f"Exception(showManageApplicantPage): {e}")