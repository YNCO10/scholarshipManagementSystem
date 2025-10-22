import sys


from PyQt6.QtWidgets import QApplication
from applicantDashbordCode import ApplicantDash

app = QApplication(sys.argv)
win = ApplicantDash()
win.showMaximized()
app.exec()