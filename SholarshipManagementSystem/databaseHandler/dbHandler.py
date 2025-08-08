import mysql.connector as conn
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox
from mysql.connector import Error


class databaseHandler:
    def __init__(self, host, user, password, databaseName):
        try:
            self.myConn = conn.connect(
                host=host,
                user=user,
                password=password,
                database=databaseName
            )

            self.cursor = self.myConn.cursor()
            print("Connection Successful")
            self.msgBox("Successful", "Database Connection Successful")
        except Error as e:
            self.myConn = None
            self.cursor = None

            print(f"Connection Failed:\n{e}")
            self.msgBox("Con Failed", "No database connection.")



    def insert(self, query, values):

        if self.myConn:
            try:

                self.cursor.execute(query, values or ())
                self.myConn.commit()
                print("Insert successful.")
                self.msgBox("Successful", "Insert Successful")

            except Error as e:

                print(f"Insert Failed: {e}")
                self.msgBox("Failed", f"Insert Failed: {e}")

        else:

            print("Insert failed: No database connection.")
            self.msgBox("Con Failed", "No database connection.")




    def select(self, query, values=None):
        if self.myConn:
            try:

                self.cursor.execute(query, values or ())
                result = self.cursor.fetchall()
                self.msgBox("Successful", "Select Successful")
                return result

            except Error as e:

                print(f"Select Failed: {e}")
                self.msgBox("Failed", f"Select Failed: {e}")

        else:

            print("Select failed: No database connection.")
            self.msgBox("Con Failed", "No database connection.")

        return []





    def delete(self, query, values=None):
        if self.myConn:
            try:
              self.cursor.execute(query, values or ())
              self.myConn.commit()
              print("Delete successful.")
              self.msgBox("Successful", "Delete Successful")
            except Error as e:
                print(f"Select Failed: {e}")
                self.msgBox("Failed", f"Delete Failed: {e}")
        else:
            print("Delete failed: No database connection.")
            self.msgBox("Con Failed", "No database connection.")


    # MSG DIALOG
    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()