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
        return response.json()


########################################################################################################################
    def approveApplication(self):
        pass

########################################################################################################################
    def sendNotification(self):
        pass