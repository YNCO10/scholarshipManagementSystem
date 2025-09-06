import requests

class ApplicantTracker:
    def __init__(self, email, url):
        self.email = email
        self.url = url

    def getData(self):
            response = requests.post(
                self.url,
                data=self.toDict()
            )
            try:
                return response.json()
            except ValueError:
                return {"status": "error", "message": response.text}

    def toDict(self):
        return{
            "email": self.email
        }