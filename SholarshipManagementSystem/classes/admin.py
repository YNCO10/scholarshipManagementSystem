import json
import requests

class Admin:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
########################################################################################################################
    def toDict(self):
        return {
            "name":self.name,
            "email":self.email,
            "pass":self.password
        }

########################################################################################################################
    def execute(self, url):
        response = requests.post(
            url,
            data=self.toDict()
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}


########################################################################################################################
    def approveApplication(self):
        pass

########################################################################################################################
    def sendSingleNotification(self, recipientEmail, title, msg):
        url = "http://localhost/BackEnd/scholarshipManagement/notifications/insertNotification.php"
        response = requests.post(
            url=url,
            data={
                "email": self.email,
                "recipientEmail": recipientEmail,
                "title": title,
                "msg": msg
            }
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}

##################################################################################h#######################################
    def updateDetails(self, category, value):
        response = requests.post(
            "http://localhost/BackEnd/scholarshipManagement/profile/updateDetails.php",
            data={
                "cat" : category,
                "email" : self.email,
                "value" : value
            }
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}

########################################################################################################################
    def getAdminDetails(self):
        response = requests.post(
            "http://localhost/BackEnd/scholarshipManagement/admin/getDetails.php",
            data={
                "email" : self.email
            }
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}

########################################################################################################################
    def bulkNotificationsForApplicants(self, senderEmail, title, message, recipientEmails):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/notifications/insertNotificationsInBulk.php",
                data={
                    "email": senderEmail,
                    "title": title,
                    "msg": message,
                    "recipientEmails": json.dumps(recipientEmails)
                }
            )
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}