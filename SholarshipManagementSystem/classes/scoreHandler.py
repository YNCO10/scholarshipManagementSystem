class ScoreHandler:
    def __init__(self,
                 academicWeight,
                 financialWeight,
                 assessmentWeight):
        self.academicWeight = academicWeight
        self.financialWeight = financialWeight
        self.assessmentWeight = assessmentWeight

########################################################################################################################
    def AcademicScore(self,gpa):
        return (gpa / 5) * 100

########################################################################################################################
    def financialScore(self, need: bool, incomeBracket = None):
        if need == 0:
            return 0

        score = 50 #threshold for whether they need support or not

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
    # def documentScore(self, uploadedDocs:list, requiredDocs:list)->float:
    #     if not requiredDocs:
    #         return 0
    #     uploadedCount = sum(1 for d in requiredDocs if d in uploadedDocs)
    #     return (uploadedCount/len(requiredDocs)) * 100

########################################################################################################################
    def assessmentScore(self, score:int, total:int)->float:
        if total == 0:
            return 0
        return score/total*100

########################################################################################################################
    def applicantScore(self, applicantInfo:dict):
        academicScore = self.AcademicScore(
            applicantInfo["gpa"]
        )
        financialScore = self.financialScore(
            applicantInfo["need"],
            applicantInfo["incomeBracket"]
        )
        assessmentScore = self.assessmentScore(
            applicantInfo["assessmentScore"],
            applicantInfo["totalQuest"]
        )

        totalWeights = self.academicWeight +self.financialWeight +self.assessmentWeight #+self.documentWeight

        finalScore = (
            academicScore * self.academicWeight+
            financialScore * self.financialWeight+
            assessmentScore * self.assessmentWeight
        ) / totalWeights

        return round(finalScore, 0)