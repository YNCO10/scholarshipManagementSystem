import os
from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrinter


class Report:

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