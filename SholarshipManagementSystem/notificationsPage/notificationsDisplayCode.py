import requests
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.notificationsPage.notificationsDisplayPage import Ui_NotificationDisplay
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode

class NotificationDisplay(QWidget, Ui_NotificationDisplay):
    def __init__(self, Id):
        super().__init__()
        self.appDash = None
        self.setupUi(self)
        self.Id = Id
        self.regCode = RegCode()
        self.setWindowTitle("Notifications")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))

        self.populateNotificationPage()
        self.btnClicks()

########################################################################################################################
    def btnClicks(self):
        self.cancelBtn.clicked.connect(self.updateNotificationStatus)

########################################################################################################################
    def populateNotificationPage(self):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/notifications/getNotificationUsingID.php",
                data={
                    "id": self.Id
                }
            )

            result = response.json()
            msg = result.get("message")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    f"{msg}"
                )
                print(f"Error: {msg}")
                return

            dbContent = result.get("data")
            item = dbContent[0]

            self.recipientLabel.setText(f"To: {item.get("recipient_email")}")
            self.senderLabel.setText(f"From: {item.get("sender_name")}")
            self.msgLabel.setText(item.get("msg"))
            self.titleLabel.setText(f"Message Title: {item.get("title")}")
            self.statusLabel.setText(f"Message Title: {item.get("noti_status")}")

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception: {e}"
            )
            print(f"Error: {e}")

########################################################################################################################
    def updateNotificationStatus(self):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/notifications/updateNotificationStatus.php",
                data={
                    "id": self.Id
                }
            )

            result = response.json()
            msg = result.get("message")

            if result.get("status") == "success":
                print(f"{msg}")
                from SholarshipManagementSystem.homePage.applicantDashbordCode import ApplicantDash
                self.appDash = ApplicantDash()
                self.appDash.switchToNotifications("")
                self.close()

            else:
                self.regCode.msgBox(
                    "Error",
                    f"{msg}"
                )
                print(f"Error: {msg}")
                self.close()
        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(updateNotificationStatus): {e}"
            )
            print(f"Error(updateNotificationStatus): {e}")