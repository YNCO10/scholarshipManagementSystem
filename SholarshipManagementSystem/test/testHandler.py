from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.authentications.loginValidationPHP import LoginCode
import unittest


class TestHandler(unittest.TestCase):
    def testLogin(self):

        login = LoginCode()
        result = login.login()
        self.assertTrue(result)

    def testRegistration(self):
        regCode = RegCode()
        result = regCode.register()
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()