class Assessment:
    def __init__(self,questions):

        self.questions = questions
        self.current_index = 0
        self.score = 0
########################################################################################################################
    def getQuestion(self):
        return self.questions[self.current_index]

########################################################################################################################
    def checkAns(self, userAns):
        correctAns = self.questions[self.current_index]["ans"]
        if userAns == correctAns:
            self.score += 1
        return userAns == correctAns

########################################################################################################################
    def nextQuestion(self):
        self.current_index += 1

        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

########################################################################################################################
    def finalScore(self):
        return self.score