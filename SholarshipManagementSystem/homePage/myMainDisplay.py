import json
import os
import subprocess
import sys

import requests
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, \
    QVBoxLayout
from SholarshipManagementSystem.homePage.dashboard import Ui_MainWindow
from matplotlib.figure import Figure
import Sessions
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas



class Dash(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Dashboard")

        self.passTxt.setText("THIS IS A RANDOM PASSWORD NIGGA")

        #DISPLAY HOME SCREEN
        self.mainDisplayWidget.setCurrentIndex(0)
        self.populateApplicantTbl()
        self.homeBtn.click()
        self.homeIconBtn.click()

        self.iconNameWidget.setHidden(True)

        # DISPLAY USERNAME
        self.usernameLabel.setText(Sessions.adminName)
        self.homeScreenUsernameLabel.setText(f"Hello {Sessions.adminName}")


        #BTN CLICKS
        self.BtnClicks()
        self.readOnlyLineEdit()
        self.loadPlot()
        self.loadPlot2()

        self.listofApplicantsTableWidget.setFixedHeight(300)
        self.chartWidget.setFixedHeight(300)
        self.chart2Widget.setFixedHeight(300)




    #BTN CLICKS###############################################################
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
    #     show password
        self.showPassBtn.clicked.connect(self.togglePasswordBtn)

    ###PASSWORD#########################################################################################################
    def togglePasswordBtn(self):
        if self.passTxt.echoMode() == QLineEdit.EchoMode.Normal:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Password)
            self.showPassBtn.setIcon(QIcon(":icons/seeWhiteIcon.png"))
        else:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.showPassBtn.setIcon(QIcon(":icons/hideWhite.png"))


########################################################################################################################
    def readOnlyLineEdit(self):
        self.usernameTxt.setReadOnly(True)
        self.passTxt.setReadOnly(True)
        self.emailTxt.setReadOnly(True)



    # PAGE SWITCHING####################################################################################################
    def switchToDash(self):
        self.mainDisplayWidget.setCurrentIndex(0)

    def switchToScholarshipPage(self):
        self.mainDisplayWidget.setCurrentIndex(1)
        #     POPULATE TBL
        self.populateTableWidget()

    def switchToNotificationsPage(self):
        self.mainDisplayWidget.setCurrentIndex(3)

    def switchToProfilePage(self):
        self.mainDisplayWidget.setCurrentIndex(2)

    def switchToReportsPage(self):
        self.mainDisplayWidget.setCurrentIndex(4)
    # PAGE SWITCHING END################################################################################################

    # POPULATE TABLE WIDGET#############################################################################################
    def populateTableWidget(self):

        print(f"Admin Email: {Sessions.seshEmail}")
        try:
            response = requests.get("http://localhost/BackEnd/scholarshipManagement/uploadScholarships/getScholarshipDetails.php")

            print(F"RAW RESPONSE: {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown response")

            if result.get("status") == "success":
                    #     get db content
                dbContent = result.get("data",[])
                self.scholarshipTableWidget.setRowCount(len(dbContent))#always initialise tbl so it doesn't stack up rows

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
                    self.scholarshipTableWidget.setItem(rowindx, 1, QTableWidgetItem(str(rowData.get("id",""))))
                    self.scholarshipTableWidget.setItem(rowindx, 2, QTableWidgetItem(rowData.get("scholarship_name","")))
                    self.scholarshipTableWidget.setItem(rowindx, 3, QTableWidgetItem(rowData.get("descrip","")))
                    self.scholarshipTableWidget.setItem(rowindx, 4, QTableWidgetItem(rowData.get("type","")))
                    self.scholarshipTableWidget.setItem(rowindx, 5, QTableWidgetItem(rowData.get("subject","")))
                    self.scholarshipTableWidget.setItem(rowindx, 6, QTableWidgetItem(rowData.get("deadline","")))
                    self.scholarshipTableWidget.setItem(rowindx, 7, QTableWidgetItem(rowData.get("financial_amount","")))
                    self.scholarshipTableWidget.setItem(rowindx, 8, QTableWidgetItem(rowData.get("provider","")))
                    self.scholarshipTableWidget.setItem(rowindx, 9, QTableWidgetItem(rowData.get("provider_email","")))
                    self.scholarshipTableWidget.setItem(rowindx, 10, QTableWidgetItem(rowData.get("applicantion_link","")))
                    self.scholarshipTableWidget.setItem(rowindx, 11, QTableWidgetItem(rowData.get("perks","") or "No Benefits Available for this Scholarship"))
                    self.scholarshipTableWidget.setItem(rowindx, 12, QTableWidgetItem(rowData.get("file_path","")))

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
                        lambda _, path=rowData.get("file_path"):self.displayScholarshipDoc(path)
                    )
                    delBtn.clicked.connect(
                        lambda _, Id=rowData.get("id"):self.delScholarship(Id)
                    )
                    #   align horizontally
                    btnWidget = QWidget()
                    layout = QHBoxLayout(btnWidget)
                    layout.addWidget(viewBtn)
                    layout.addWidget(delBtn)
                    layout.setContentsMargins(0,0,0,0)

            #         add widget to tbl
                    self.scholarshipTableWidget.setCellWidget(rowindx, 0, btnWidget)

                self.styleTbl()



            elif result.get("message") == "error":
                self.msgBox("Error(upload)", f"Upload error: {msg}")
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


########################################################################################################################


    def plot1(self):

        url = "http://localhost/BackEnd/scholarshipManagement/authentications/dataForChart.php"

        response = requests.post(
            url = url
        )

        print(f"RAW RESPONSE : {response.text}")
        result = json.loads(response.text)
        msg = result.get("message", "Unknown error")

        if result.get("status") == "error":
            self.msgBox(
                "Error",
                msg
            )
            return

        fig = Figure()
        ax = fig.add_subplot(111)
        categories = list(result.keys())
        sizes = list(result.values())
        ax.pie(sizes, labels=categories, autopct="%1.1f%%")
        # ax.set_title("Financial Amount")
        return fig

########################################################################################################################
    def plot2(self):
        url = "http://localhost/BackEnd/scholarshipManagement/authentications/dataForChart.php"

        response = requests.post(
            url=url
        )

        print(f"RAW RESPONSE : {response.text}")
        result = json.loads(response.text)
        msg = result.get("message", "Unknown error")

        if result.get("status") == "error":
            self.msgBox(
                "Error",
                msg
            )
            return

        categories = list(result.keys())
        sizes = list(result.values())

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=categories, autopct="%1.1f%%")
        # ax.set_title("Applicant Education Levels")
        return fig

########################################################################################################################
    def plot3(self):
        url = "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/loadScholarshipCategories.php"

        response = requests.post(
            url=url
        )

        print(f"RAW RESPONSE : {response.text}")
        result = json.loads(response.text)
        msg = result.get("message", "Unknown error")

        if result.get("status") == "error":
            self.msgBox(
                "Error",
                msg
            )
            return

        # categories = list(result.keys())
        # sizes = list(result.values())
        categories = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]
        sizes = [
            5,
            4,
            12,
            7,
            7,
            2,
            6
        ]

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(categories, sizes, marker="o")


        for i, value in enumerate(sizes):
            ax.text(i, value + 1, str(value), ha='center', va='bottom')

        ax.set_title("Applicant Education Levels")
        ax.set_ylabel("Values")
        ax.set_xlabel("Financial Amount")

        return fig

########################################################################################################################
    def loadPlot(self):
        figure = FigureCanvas(self.plot1())
        layout = QVBoxLayout(self.chartWidget)
        layout.addWidget(figure)

########################################################################################################################
    def loadPlot2(self):
        figure = FigureCanvas(self.plot3())
        layout = QVBoxLayout(self.chart2Widget)
        layout.addWidget(figure)

########################################################################################################################
    def populateApplicantTbl(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/authentications/loadApplicantData.php")

            print(F"RAW RESPONSE: {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown response")

            if result.get("status") == "success":
                #     get db content
                dbContent = result.get("data", [])
                print(dbContent)
                self.listofApplicantsTableWidget.setRowCount(
                    len(dbContent))  # always initialise tbl so it doesn't stack up rows
                self.listofApplicantsTableWidget.setRowCount(len(dbContent))

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
                        "Assessment Score"
                    ]
                )

                #     populate tbl with content from db
                for rowindx, rowData in enumerate(dbContent):
                    #         fill data for all 4 columns
                    self.listofApplicantsTableWidget.setItem(rowindx, 1, QTableWidgetItem(str(rowData.get("id", ""))))
                    self.listofApplicantsTableWidget.setItem(rowindx, 2, QTableWidgetItem(rowData.get("name", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 3, QTableWidgetItem(rowData.get("email", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 4, QTableWidgetItem(str(rowData.get("age", ""))  or "Not specified"))
                    self.listofApplicantsTableWidget.setItem(rowindx, 5, QTableWidgetItem(rowData.get("gender", "") or "Not specified"))
                    self.listofApplicantsTableWidget.setItem(rowindx, 6, QTableWidgetItem(rowData.get("nationality", "") or "Not specified"))
                    self.listofApplicantsTableWidget.setItem(rowindx, 7, QTableWidgetItem(rowData.get("education_level", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 8, QTableWidgetItem(rowData.get("dob", "")))
                    self.listofApplicantsTableWidget.setItem(rowindx, 9, QTableWidgetItem(str (rowData.get("score", "")) or 0))

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

                    # viewBtn.clicked.connect(
                    #     #DISPLAY APPLICANT DETAILS WIDGET
                    # )
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
                "http://localhost/BackEnd/scholarshipManagement/authentications/deleteApplicant.php",
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
                self.msgBox("delete failed(dash)", f"{msg}")
                print(f"deleting(dash): {msg}")
        except Exception as e:
            self.msgBox("Error", f"Something went wrong while Deleting Applicant(dash): {e}")
            print(e)