from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPdf import QPdfDocument
import sys

class PDFViewer(QWidget):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("Report Viewer")

        # layout = QVBoxLayout()
        # self.setLayout(layout)
        #
        # self.web = QWebEngineView()
        # self.web.load(QUrl.fromLocalFile(path))
        # layout.addWidget(self.web)
        layout = QVBoxLayout()

        self.pdf_view = QPdfView(self)
        self.pdf_doc = QPdfDocument(self)
        self.pdf_doc.load(path)

        self.pdf_view.setDocument(self.pdf_doc)
        layout.addWidget(self.pdf_view)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer("C:/Users/Yankho/OneDrive/Desktop/PROJECT/reportLogs/report_2025-10-20_4.pdf")
    viewer.show()
    sys.exit(app.exec())