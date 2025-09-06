
class ScoreHandler:
    def __init__(self):
        self.weights = {
            "academic": 0.5,
            "financial": 0.2,
            "document": 0.15,
            "assessment": 0.15
        }

    def AcademicScore(self,gpa:int, transcript: bool)-> float:
        if not transcript:
            return 0

        return (gpa / 5.0) * 100

    def financialScore(self, need: bool, proofUploaded, incomeBracket:float = None)->float:
        if not need:
            return 0

        score = 50 #threshold for whether they need support or not

        if proofUploaded:
            score += 30

        if incomeBracket is not None:
            if incomeBracket < 150000:# adjust depending on malawi's income bracket
                score += 20

        return min(score, 100)

    def documentScore(self, uploadedDocs:list, requiredDocs:list)->float:
        if not requiredDocs:
            return 100
        uploadedCount = sum(1 for d in requiredDocs if d in uploadedDocs)
        return (uploadedCount/len(requiredDocs)) * 100

    def assessmentScore(self, correctAns:int, total:int)->float:
        if total == 0:
            return 0
        return (correctAns/total) * 100

    def applicantScore(self, applicantInfo:dict):
        academicScore = self.AcademicScore(
            applicantInfo["gpa"],
            applicantInfo["transcript"]
        )
        financialScore = self.financialScore(
            applicantInfo["need"],
            applicantInfo["financialProof"],
            applicantInfo["incomeBracket"]
        )
        documentScore = self.documentScore(
            applicantInfo["uploadedDocs"],
            applicantInfo["requiredDocs"]
        )
        assessmentScore = self.assessmentScore(
            applicantInfo["score"],
            applicantInfo["totalQuest"]
        )

        finalScore = (
            academicScore * self.weights["academic"]+
            financialScore * self.weights["financial"]+
            documentScore * self.weights["document"]+
            assessmentScore * self.weights["assessment"]
        ) / sum(self.weights.values())

        return round(finalScore, 2)