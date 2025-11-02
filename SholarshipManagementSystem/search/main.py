import requests
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode


class Search:
    def __init__(self):
        self.regCode = RegCode()
########################################################################################################################
    def executeSearch(self, url, keyword):
        try:
            response = requests.post(
                url,
                data={
                    "keyword": keyword
                }
            )
            try:
                return response.json()
            except ValueError:
                return {
                    "status":"fatalError",
                    "message":response.text
                }
        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception: {e}"
            )
            print(f"Exception: {e}")
########################################################################################################################
    def executeSearchWithEmail(self, url, keyword, email):
        try:
            response = requests.post(
                url,
                data={
                    "keyword": keyword,
                    "email" : email
                }
            )
            try:
                return response.json()
            except ValueError:
                return {
                    "status":"fatalError",
                    "message":response.text
                }
        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception: {e}"
            )
            print(f"Exception: {e}")

########################################################################################################################