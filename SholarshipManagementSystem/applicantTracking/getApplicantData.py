from SholarshipManagementSystem.classes.applicantTracking import ApplicantTracker
import Sessions

class GetApplicantData:
    def __init__(self):
        url = "http://localhost/BackEnd/scholarshipManagement/applicatTracking/getData.php"
        self.applicantTracker = ApplicantTracker(Sessions.seshEmail, url)


    def getData(self):
        result = self.applicantTracker.getData()
        msg = result.get("message")

        if result.get("status") == "success":
            applicant_data = {
                "gpa": result.get("gpa"),
                "transcript": result.get("transcript"),
                "need": result.get("need"),
                "financialProof": result.get("financialProof"),
                "incomeBracket": result.get("incomeBracket"),
                "uploadedDocs": result.get("uploadedDocs"),
                "score": result.get("score"),
            }
