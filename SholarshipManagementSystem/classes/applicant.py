import requests


class Applicant:
    def __init__(self, name, email, nationality, password, gender, phoneNum, age, dob, educationLevel):
        self.name = name,
        self.email = email,
        self.nationality = nationality,
        self.password = password,
        self.gender = gender,
        self.phoneNum = phoneNum,
        self.age = age,
        self.dob = dob,
        self.educationLevel = educationLevel


    def toDict(self):
        return {
            "name": self.name,
            "email": self.email,
            "nationality":self.nationality,
            "pass": self.password,
            "gender":self.gender,
            "phone_number":self.phoneNum,
            "age":self.age,
            "dob":self.dob,
            "education_level": self.educationLevel
        }

    def execute(self, url):
        response = requests.post(
            url,
            data=self.toDict()
        )
        return response.json()
