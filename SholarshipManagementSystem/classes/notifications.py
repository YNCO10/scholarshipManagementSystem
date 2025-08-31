class Notifications:
    def __init__(self, name, title, msg):
        self.name = name
        self.title = title
        self.msg = msg

    def sendNotification(self):
        pass

    def weeklyReport(self):
        pass

    def toDict(self):
        return {
            "name": self.name,
            "title": self.title,
            "msg": self.msg
        }