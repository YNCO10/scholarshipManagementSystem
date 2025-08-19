from SholarshipManagementSystem.welcomePage.welcomePageCode import WelcomePageCode
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.authentications.regApplicantValidationPHP import AppValCode
from SholarshipManagementSystem.authentications.loginValidationPHP import LoginCode

class Controller:
    def __init__(self):
        self.welcome = WelcomePageCode()
        self.adminReg = RegCode()
        self.applicantReg = AppValCode()
        self.login = LoginCode()

        self.btnClicks()

    def btnClicks(self):
        # btns in welcome page
        self.welcome.goToAdminRegBtn.clicked.connect(self.showAdminReg)

        self.welcome.goToApplicantRegBtn.clicked.connect(self.showApplicantReg)

        self.welcome.goToLoginBtn.clicked.connect(self.showLogin)

        #     btn in admin reg
        self.adminReg.goToLoginPageBtn.clicked.connect(self.showLogin)

        # applicant reg
        self.applicantReg.goToLoginPageBtn.clicked.connect(self.showLogin)

        # login
        self.login.goToRegistrationPageBtn.clicked.connect(self.showWelcome)


    def showWelcome(self):
        self.hideAll()
        self.welcome.show()

    def showAdminReg(self):
        self.hideAll()
        self.adminReg.show()

    def showApplicantReg(self):
        self.hideAll()
        self.welcome.hide()
        self.applicantReg.show()

    def showLogin(self):
        self.hideAll()
        self.login.show()

    def hideAll(self):
        self.adminReg.hideWindow()
        self.welcome.hideWindow()
        self.applicantReg.hideWindow()
        self.login.hideWindow()
