import json

import requests



class Scholarships:
    def __init__(self,
                 name,
                 type,
                 path,
                 deadline,
                 descrip,
                 provider,
                 financialAmount,
                 applicationLink,
                 providerEmail,
                 subject
                 ):

        self.name = name
        self.path = path
        self.type = type
        self.deadline = deadline
        self.descrip = descrip
        self.provider = provider
        self.financialAmount = financialAmount
        self.applicationLink = applicationLink
        self.providerEmail = providerEmail
        self.subject = subject

    def execute(self, url, filepath, selectedPerks = None, email = None):
        if selectedPerks is None:
            selectedPerks = []

        response = requests.post(
            url,
            data=self.toDict(selectedPerks, email),
            files={
                "document": open(filepath, "rb")
            }
        )
        print(f"RAW RESPONSE: {response.text}")
        return response.json()

    def toDict(self, selectedPerks = None, email = None):
        if selectedPerks is None:
            selectedPerks = []
        return {
            "name": self.name,
            "type": self.type,
            "path": self.path,
            "deadline": self.deadline,
            "descrip": self.descrip,
            "provider": self.provider,
            "financialAmount": self.financialAmount,
            "applicationLink": self.applicationLink,
            "providerEmail": self.providerEmail,
            "subject": self.subject,
            "perks": json.dumps(selectedPerks),
            "email": email
        }