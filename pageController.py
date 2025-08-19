from SholarshipManagementSystem.welcomePage.welcomePageCode import WelcomePageCode
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.authentications.regApplicantValidationPHP import AppValCode
from SholarshipManagementSystem.authentications.loginValidationPHP import LoginCode
from SholarshipManagementSystem.homePage.myMainDisplay import Dash
from SholarshipManagementSystem.manageScholarshipsPage.uploadScholarCode import UploadingCode
import myProjectResources

class Controller:
    def __init__(self):
        self.welcome = WelcomePageCode()
        self.adminReg = RegCode()
        self.applicantReg = AppValCode()
        self.login = LoginCode()
        self.adminHome = Dash()
        self.uploadScholar = UploadingCode()

        # btn clicks
        self.btnClicksLogin()
        self.btnClicksWelcome()
        self.btnClicksAppReg()
        self.btnClicksAdminReg()
        self.btnClicksAdminDash()



    # btn clicks#################################################################
    def btnClicksLogin(self):
        # login
        self.login.goToRegistrationPageBtn.clicked.connect(self.showWelcome)

    ###############################################################################
    def btnClicksAppReg(self):
        # applicant reg
        self.applicantReg.goToLoginPageBtn.clicked.connect(self.showLogin)

    ###############################################################################
    def btnClicksAdminReg(self):
        #     btn in admin reg
        self.adminReg.goToLoginPageBtn.clicked.connect(self.showLogin)

   ###############################################################################
    def btnClicksWelcome(self):
        # btns in welcome page
        self.welcome.goToAdminRegBtn.clicked.connect(self.showAdminReg)

        self.welcome.goToApplicantRegBtn.clicked.connect(self.showApplicantReg)

        self.welcome.goToLoginBtn.clicked.connect(self.showLogin)

    ###############################################################################
    def btnClicksAdminDash(self):
        self.adminHome.uploadScholarshipBtn.clicked.connect(self.showUploadScholarship)




    # SHOW/HIDE WINDOWS##################################################################
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

    def showAdinDash(self):
        self.hideAll()
        self.adminHome.show()

    def showUploadScholarship(self):
        self.hideAll()
        self.uploadScholar.show()


    def hideAll(self):
        self.adminReg.hideWindow()
        self.welcome.hideWindow()
        self.applicantReg.hideWindow()
        self.login.hideWindow()


