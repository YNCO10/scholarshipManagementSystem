import json
import requests


class Applicant:
    def __init__(self,
                 name,
                 email,
                 nationality,
                 password,
                 gender,
                 phoneNum,
                 age,
                 dob,
                 educationLevel,
                 gpa,
                 schoolAttended,
                 incomeBracket,
                 program
                 ):
        self.name = name
        self.email = email
        self.nationality = nationality
        self.password = password
        self.gender = gender
        self.phoneNum = phoneNum
        self.age = age
        self.dob = dob
        self.educationLevel = educationLevel
        self.gpa = gpa
        self.schoolAttended = schoolAttended
        self.incomeBracket = incomeBracket
        self.program = program

##################################################################################h#####################################
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
            "education_level": self.educationLevel,
            "gpa": self.gpa,
            "schoolAttended": self.schoolAttended,
            "incomeBracket": self.incomeBracket,
            "program" : self.program
        }

##################################################################################h#####################################
    def execute(self, url):
        response = requests.post(
            url,
            data=self.toDict()
        )
        return response.json()

##################################################################################h#####################################
    def updateDetails(self, category, value):
        response = requests.post(
            "http://localhost/BackEnd/scholarshipManagement/profile/updateApplicantDetails.php",
            data={
                "cat": category,
                "email": self.email,
                "value": value
            }
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}

########################################################################################################################

    def getApplicantDetailsDB(self):
        response = requests.post(
            "http://localhost/BackEnd/scholarshipManagement/applicant/allApplicantDetails.php",
            data={
                "email": self.email
            }
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response was not JSON:", response.text)
            return {"status": "error", "message": "Invalid server response"}