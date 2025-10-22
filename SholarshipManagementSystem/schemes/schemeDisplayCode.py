import requests
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.schemes.schemeDisplayPage import Ui_Form
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode


class SchemeDetails(QWidget, Ui_Form):
    def __init__(self, Id):
        super().__init__()
        self.Id = Id
        self.regCode = RegCode()
        self.setupUi(self)
        self.setWindowTitle("Scheme Details")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.btnClicks()
        self.populateSchemePage()

########################################################################################################################
    def btnClicks(self):
        self.cancelBtn.clicked.connect(self.closeWindow)

########################################################################################################################
    def populateSchemePage(self):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/chartData/schemeDataWithID.php",
                data={
                    "id" : self.Id
                }
            )
            print(f"RAW RESPONSE: {response.text}")
            result = response.json()
            msg = result.get("message")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                return
            dbContent = result.get("data")
            item = dbContent[0]

            self.schemeNameLabel.setText(f"SCHEME NAME\n{item.get("scheme_name")}")
            self.schemeDescriptionLabel.setText(f"{item.get("description")}")
            self.benefitDetailsLabel.setText(f"{item.get("benefit_details")}")

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(populateSchemeTbl): {e}"
            )

########################################################################################################################
    def closeWindow(self):
        self.close()