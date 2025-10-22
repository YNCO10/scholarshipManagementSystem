import os
import requests
from PyQt6.QtGui import QPainter
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from SholarshipManagementSystem.authentications.regValidationPHP import RegCode


class Report:

    def __init__(self):
        self.pdf_doc = None
        self.pdf_view = None
        self.regCode = RegCode()

    def generateReport(self, scrollArea, fileName):
        print("checkpoint 1")
        myPath = "C:/Users/Yankho/OneDrive/Desktop/PROJECT/reportLogs"

        #makesure directory exists else create it
        os.makedirs(myPath, exist_ok=True)

        #if filename doesn't end with .pdf then add the extension
        if not fileName.endswith(".pdf"):
            fileName += ".pdf"

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        #bind filepath with filename
        filePath = os.path.join(myPath, fileName)

        #add filepath to printer
        printer.setOutputFileName(filePath)

        # High resolution for crisp output
        printer.setResolution(300)

        reportWidget = scrollArea.widget()
        #check if widget exists
        if reportWidget is None:
            print("No widget found in scrollArea! Report generation aborted.")
            return

        total_height = reportWidget.height()
        total_width = reportWidget.width()

        # create painter
        painter = QPainter(printer)

        page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)

        scale = page_rect.width() / total_width
        painter.scale(scale, scale)

        page_height = page_rect.height() / scale  # scaled page height
        y_offset = 0

        while y_offset < total_height:
            # Render a "slice" of the widget onto the current page
            painter.save()
            painter.translate(0, -y_offset)
            reportWidget.render(painter)
            painter.restore()

            y_offset += page_height
            if y_offset < total_height:
                printer.newPage()

        painter.end()

        print(f"Process Complete.\nReport has been saved at {filePath}")

########################################################################################################################
    def generateReportForApplicant(self, scrollArea, fileName):
        print("checkpoint 1")
        myPath = "C:/Users/Yankho/OneDrive/Desktop/PROJECT/reportLogs/applicantReports"

        #makesure directory exists else create it
        os.makedirs(myPath, exist_ok=True)

        #if filename doesn't end with .pdf then add the extension
        if not fileName.endswith(".pdf"):
            fileName += ".pdf"

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        #bind filepath with filename
        filePath = os.path.join(myPath, fileName)

        #add filepath to printer
        printer.setOutputFileName(filePath)

        # High resolution for crisp output
        printer.setResolution(300)

        reportWidget = scrollArea.widget()
        #check if widget exists
        if reportWidget is None:
            print("No widget found in scrollArea! Report generation aborted.")
            return

        total_height = reportWidget.height()
        total_width = reportWidget.width()

        # create painter
        painter = QPainter(printer)

        page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)

        scale = page_rect.width() / total_width
        painter.scale(scale, scale)

        page_height = page_rect.height() / scale  # scaled page height
        y_offset = 0

        while y_offset < total_height:
            # Render a "slice" of the widget onto the current page
            painter.save()
            painter.translate(0, -y_offset)
            reportWidget.render(painter)
            painter.restore()

            y_offset += page_height
            if y_offset < total_height:
                printer.newPage()

        painter.end()

        print(f"Process Complete.\nReport has been saved at {filePath}")

########################################################################################################################
    def populateReportLogs(self, role, tblWidget, email, widget):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/reports/getReports.php",
                data={
                    "role" : role,
                    "email" : email
                }
            )
            print(F"RAW RESPONSE(populateReportLogs): {response.text}")
            result = response.json()
            msg = result.get("message")

            if result.get("status") == "success":

                dbContent = result.get("data")
                tblWidget.setColumnCount(5)
                tblWidget.setRowCount(len(dbContent))

                tblWidget.setHorizontalHeaderLabels([
                    "Actions",
                    "ID",
                    "Name",
                    "Date Created",
                    "File Path"
                ])

                for rowIdx, rowData in enumerate(dbContent):
                    tblWidget.setItem(rowIdx, 1, QTableWidgetItem(str(rowData.get("id", ""))))
                    tblWidget.setItem(rowIdx, 2, QTableWidgetItem(rowData.get("name", "")))
                    tblWidget.setItem(rowIdx, 3, QTableWidgetItem(rowData.get("date_created", "")))
                    tblWidget.setItem(rowIdx, 4, QTableWidgetItem(rowData.get("filepath", "")))

                    viewBtn = QPushButton("View")

                    viewBtn.setStyleSheet("QPushButton { "
                                          "color: white;"
                                          "background-color: #010e1b;"
                                          "padding:3px;"
                                          "margin:0px;"
                                          "border-radius:3px;"
                                          "}")

                    viewBtn.clicked.connect(
                        lambda _, path=rowData.get("filepath"): self.displayReport(path, widget)
                    )

                    btnWidget = QWidget()
                    layout = QHBoxLayout(btnWidget)
                    layout.addWidget(viewBtn)
                    layout.setContentsMargins(0, 0, 0, 0)

                    #         add widget to tbl
                    tblWidget.setCellWidget(rowIdx, 0, btnWidget)

                tblWidget.setStyleSheet("QTableWidget { color: #010e1b; }")
                tblWidget.resizeColumnsToContents()

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    f"{msg}"
                )
        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(populateReportLogs): {e}"
            )
            print(f"Exception(populateReportLogs):{e}")

########################################################################################################################
    def displayReport(self, path, widget):
        #use existing layout
        layout = widget.layout()

        # create layout if layout doesn't exist
        if layout is None:
            layout = QVBoxLayout(widget)
            widget.setLayout(layout)

        # Clear previous PDF viewer
        for i in reversed(range(layout.count())):
            old_widget = layout.itemAt(i).widget()
            if old_widget is not None:
                old_widget.deleteLater()

        self.pdf_view = QPdfView(widget)
        self.pdf_doc = QPdfDocument(widget)
        self.pdf_doc.load(path)

        self.pdf_view.setDocument(self.pdf_doc)
        layout.addWidget(self.pdf_view)