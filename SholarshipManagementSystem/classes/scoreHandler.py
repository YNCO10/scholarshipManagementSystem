class ScoreHandler:
    def __init__(self,
                 academicWeight,
                 financialWeight,
                 assessmentWeight):
        self.academicWeight = academicWeight
        self.financialWeight = financialWeight
        self.assessmentWeight = assessmentWeight

########################################################################################################################
    def overallAvgScore(self, sumApplicantScores, applicantScoresLen):
        return sumApplicantScores / applicantScoresLen

########################################################################################################################
    def calculateSuccessPrediction(self, applicantScore):
        if applicantScore > 79:
            return "Very Likely"
        elif applicantScore > 59:
            return "likely"
        elif applicantScore > 39:
            return "Unlikely"
        else:
            return "Very unlikely"

########################################################################################################################
    def calculateEligibility(self, avg, applicantScore):
        if applicantScore >= avg:
            return "Eligible"
        else:
            return "Not Eligible"

########################################################################################################################
    def AcademicScore(self,gpa):
        return (gpa / 5) * 100

########################################################################################################################
    def financialScore(self, need: bool, incomeBracket = None):
        if need == 1:
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
    def assessmentScore(self, score:int, total:int)->float:
        if total == 0:
            return 0
        return score/total * 100

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

        totalWeights = self.academicWeight +self.financialWeight +self.assessmentWeight

        finalScore = (
            academicScore * self.academicWeight+
            financialScore * self.financialWeight+
            assessmentScore * self.assessmentWeight
        ) / totalWeights

        return round(finalScore, 0)