from SholarshipManagementSystem.classes.scoreHandler import ScoreHandler

scoreHandler = ScoreHandler()

applicant_data = {
    "gpa": 3.7,
    "transcript": True,
    "need": True,
    "financialProof": False,
    "incomeBracket": 2000,
    "uploadedDocs": ["id_card", "transcript", "recommendation"],
    "requiredDocs": ["NationalID", "transcript", "recommendation", "proofOfNeed"],
    "score": 15,#make assessment tbl, in assessment.py, if user ends at compulsory then total questions = 20 else it's equal to 40(depending on num o questions in assessments)
    "totalQuest": 20
}

score = scoreHandler.applicantScore(applicant_data)
print("Final Applicant Score:", score)
