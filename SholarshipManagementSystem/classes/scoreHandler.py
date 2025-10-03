class ScoreHandler:
    def __init__(self,
                 academicWeight,
                 financialWeight,
                 documentWeight,
                 assessmentWeight):
        self.academicWeight = academicWeight
        self.financialWeight = financialWeight
        self.documentWeight = documentWeight
        self.assessmentWeight = assessmentWeight

########################################################################################################################
    def AcademicScore(self,gpa:int, transcript: bool)-> float:
        if transcript:
            return (gpa / 5.0) * 100
        else:
            return 0

########################################################################################################################
    def financialScore(self, need: bool, proofUploaded, incomeBracket= None):
        if not need:
            return 0

        score = 50 #threshold for whether they need support or not

        if proofUploaded:
            score += 30

        if incomeBracket is not None:
            if incomeBracket == "veryLow":
                score += 20
            elif incomeBracket == "low":
                score += 15
            elif incomeBracket == "average":
                score += 10
            elif incomeBracket == "aboveAverage":
                score += 5
            else:
                score += 2
        else:
            score -= 30

        return min(score, 100)

########################################################################################################################
    def documentScore(self, uploadedDocs:list, requiredDocs:list)->float:
        if not requiredDocs:
            return 0
        uploadedCount = sum(1 for d in requiredDocs if d in uploadedDocs)
        return (uploadedCount/len(requiredDocs)) * 100

########################################################################################################################
    def assessmentScore(self, score:int, total:int)->float:
        if total == 0:
            return 0
        return (score/total) * 100

########################################################################################################################
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
            applicantInfo["assessmentScore"],
            applicantInfo["totalQuest"]
        )

        totalWeights = self.academicWeight +self.financialWeight +self.documentWeight +self.assessmentWeight

        finalScore = (
            academicScore * self.academicWeight+
            financialScore * self.financialWeight+
            documentScore * self.documentWeight+
            assessmentScore * self.assessmentWeight
        ) / totalWeights

        return round(finalScore, 0)