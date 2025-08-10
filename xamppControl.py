import subprocess
import os

XAMPP_PATH = r"C:\XAMPP"

def start_mysql():
    subprocess.run([os.path.join(XAMPP_PATH, "mysql_start.bat")], shell=True)

def stop_mysql():
    subprocess.run([os.path.join(XAMPP_PATH, "mysql_stop.bat")], shell=True)

def start_apache():
    subprocess.run([os.path.join(XAMPP_PATH, "apache_start.bat")], shell=True)

def stop_apache():
    subprocess.run([os.path.join(XAMPP_PATH, "apache_stop.bat")], shell=True)

# Example usage:
# start_mysql()
# start_apache()
