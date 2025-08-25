import json
import os
import subprocess
import sys

import requests
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout

from SholarshipManagementSystem.homePage.dashboard import Ui_MainWindow
import Sessions

class Dash(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Dashboard")

        self.passTxt.setText("THIS IS A RANDOM PASSWORD NIGGA")

        #DISPLAY HOME SCREEN
        self.mainDisplayWidget.setCurrentIndex(0)
        self.homeBtn.click()
        self.homeIconBtn.click()

        self.iconNameWidget.setHidden(True)

        #BTN CLICKS
        self.BtnClicks()
        self.readOnlyLineEdit()





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

    ###PASSWORD######################################################################
    def togglePasswordBtn(self):
        if self.passTxt.echoMode() == QLineEdit.EchoMode.Normal:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Password)
            self.showPassBtn.setIcon(QIcon(":icons/seeWhiteIcon.png"))
        else:
            self.passTxt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.showPassBtn.setIcon(QIcon(":icons/hideWhite.png"))


###################################################################################
    def readOnlyLineEdit(self):
        self.usernameTxt.setReadOnly(True)
        self.passTxt.setReadOnly(True)
        self.emailTxt.setReadOnly(True)



    # PAGE SWITCHING#############################################################
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
    # PAGE SWITCHING END########################################################

    # POPULATE TABLE WIDGET#####################################################
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

                self.scholarshipTableWidget.setRowCount(len(dbContent))

                self.scholarshipTableWidget.setColumnCount(6)#always initialise tbl so it doesn't stack up rows

                self.scholarshipTableWidget.setHorizontalHeaderLabels(
                    ["ID", "Name", "Descrip", "File Path", "Deadline", "Actions"]
                )

                    #     populate tbl with content from db
                for rowindx, rowData in enumerate(dbContent):
                    #         fill data for all 4 columns
                    self.scholarshipTableWidget.setItem(rowindx, 0, QTableWidgetItem(str(rowData.get("id",""))))
                    self.scholarshipTableWidget.setItem(rowindx, 1, QTableWidgetItem(rowData.get("name","")))
                    self.scholarshipTableWidget.setItem(rowindx, 2, QTableWidgetItem(rowData.get("type","")))
                    self.scholarshipTableWidget.setItem(rowindx, 3, QTableWidgetItem(rowData.get("file_path","")))
                    self.scholarshipTableWidget.setItem(rowindx, 4, QTableWidgetItem(rowData.get("deadline","")))

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
                    self.scholarshipTableWidget.setCellWidget(rowindx, 5, btnWidget)

                self.styleTbl()



            elif result.get("message") == "error":
                self.msgBox("Error(upload)", f"Upload error: {msg}")
                print(msg)

        except Exception as e:
            self.msgBox("Error", f"Something went wrong Populating tbl(dash): {e}")
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



    ### DELETE SCHOLARSHIPS########################################################################################
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
                self.msgBox("Process Complete", f"{msg}")
                print(f"Delete successful: {msg}")
                self.populateTableWidget()

            elif result.get("status") == "error":
                self.msgBox("delete failed(dash)", f": {msg}")
                print(f"deleting(dash): {msg}")



        except Exception as e:
            self.msgBox("Error", f"Something went wrong while deleting(dash): {e}")
            print(f"deleting(dash): {e}")


####TABLE STYLESHEET###########################################################################
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



    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()