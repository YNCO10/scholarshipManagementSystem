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
    def sendNotification(self):
        pass