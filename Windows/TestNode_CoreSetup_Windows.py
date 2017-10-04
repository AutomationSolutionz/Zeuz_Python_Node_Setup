# Copyright 2015, Automation Solutionz
# ---

import subprocess
import shutil
import os
import sys
import platform
import commands
from subprocess import PIPE, Popen

install_str = "python -m pip install -U"

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""
    
    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    else:
        command = cmd
    print "installing: %s " %command
    print cmdline(command)

def Installer_With_Pip():
    #upgrade pip itself
    
    pip_module_list = ["pip","psutil", "pillow", "pyserial", "numpy","imutils", "simplejson","urllib3","selenium","requests", "poster","wheel" , "python3-xlib", "pyautogui", "Appium-Python-Client", "lxml", "gi","xlrd"]
    pip_module_win_only = ["pythonnet","wmi","pyautoit","pywinauto", "pypiwin32", "winshell"]
    
    for each in pip_module_list:
        try:
            install(type="pip", module_name=each)
        except:
            print "unable to install/update %s"%each


    for each in pip_module_win_only:
        try:
            install(type="pip", module_name=each)
        except:
            print "unable to install/update %s"%each

def Installer_With_Exe():
    
    list_of_exe_link = [
                        "https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe",
                        "http://downloads.sourceforge.net/wxpython/wxPython3.0-win32-3.0.2.0-py27.exe"
                        ]
    for each in list_of_exe_link:
        try:
            easy_install = "easy_install " + each 
            install(cmd=easy_install)
        except:
            print "unable to install/update %s"%each
    
def Selenium_Driver_Files_Windows():
    Chrom_Driver_Download()
    Ie_Driver_Download()
    Firefox_Driver_Download()
    selenium_Server_StandAlone_Driver_Download()
    
def Ie_Driver_Download():
    import urllib3
    http = urllib3.PoolManager()
    try:
        print "Getting latest version of IE driver"
        r = http.request('GET', 'http://selenium-release.storage.googleapis.com')
        tmp = r.data.split('/IEDriverServer_Win32')[:-1]
        latest_version = tmp[-1].split('Key>')[-1]
        print "latest version is: %s"%latest_version
    except:
        print "Unable to get the latest version."
        return
    download_link = ('http://selenium-release.storage.googleapis.com/%s/IEDriverServer_Win32_%s.0.zip')%(latest_version,latest_version)
    download_link = str(download_link)
    print "Downloading latest IE 32 bit driver from: %s" %download_link
    path = r'C:\Python27\Scripts\IEdriver_win32.zip'
    try:
        with http.request('GET', download_link, preload_content=False) as r, open(path, 'wb') as out_file:       
            shutil.copyfileobj(r, out_file)
        print "Successfully download the file: %s"%path     
        unzip(path,r'C:\Python27\Scripts')  
    except:
        print "Unable to download: %s "%download_link

def Firefox_Driver_Download():
    import urllib3
    http = urllib3.PoolManager()
    import re
    try:
        print "Getting latest version of Firefox driver"
        r = http.request('GET', 'https://github.com/mozilla/geckodriver/releases/latest')
        raw_data = str(r.data).split('\n')
        
        for each in raw_data:
            if '<span class="css-truncate-target">v' in each:
                result = re.search('<span class="css-truncate-target">(.*)</span>', each)
                latest_version = result.group(1)
                print "Latest geckodriver for Firefox is: %s"%latest_version
                break    
    except:
        print "Unable to get the latest version."
        return "failed"
    download_link = ('https://github.com/mozilla/geckodriver/releases/download/%s/geckodriver-%s-win64.zip')%(latest_version,latest_version)
    download_link = str(download_link)
    print "Downloading latest 64bit geckodriver from: %s" %download_link
    path = r'C:\Python27\Scripts\geckodriver.zip'
    try:
        with http.request('GET', download_link, preload_content=False) as r, open(path, 'wb') as out_file:       
            shutil.copyfileobj(r, out_file)
        print "Successfully download the file: %s"%path     
        unzip(path,r'C:\Python27\Scripts')  
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail

def Chrom_Driver_Download():
    import urllib3
    http = urllib3.PoolManager()
    try:
        print "Getting latest version of chrome driver"
        r = http.request('GET', 'http://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        latest_version = r.data.split('\n')[0]
        print "latest version is: %s"%latest_version
    except:
        print "Unable to get the latest version."
        return
    download_link = ('http://chromedriver.storage.googleapis.com/%s/chromedriver_win32.zip')%latest_version
    print "Downloading latest Chrom 32 bit driver from: %s" %download_link
    path = r'C:\Python27\Scripts\chromedriver_win32.zip'
    try:
        with http.request('GET', download_link, preload_content=False) as r, open(path, 'wb') as out_file:       
            shutil.copyfileobj(r, out_file)
        print "Successfully download the file: %s"%path     
        unzip(path,r'C:\Python27\Scripts')  
    except:
        print "Unable to download: % "%download_link

def selenium_Server_StandAlone_Driver_Download():
    import urllib3
    http = urllib3.PoolManager()
    try:
        print "Getting latest version of Selenium Server Standalone driver"
        r = http.request('GET', 'http://selenium-release.storage.googleapis.com')
        tmp = r.data.split('/selenium-server-standalone')[:-1]
        latest_version = tmp[-1].split('Key>')[-1]
        print "latest version is: %s"%latest_version
    except:
        print "Unable to get the latest version."
        return
    download_link = ('http://selenium-release.storage.googleapis.com/%s/selenium-server-standalone-%s.0.jar')%(latest_version,latest_version)
    download_link = str(download_link)
    print "Downloading latest selenium_Server_StandAlone: %s" %download_link
    path = r'C:\Python27\Scripts\selenium-server-standalone.jar'
    try:
        with http.request('GET', download_link, preload_content=False) as r, open(path, 'wb') as out_file:       
            shutil.copyfileobj(r, out_file)  
        print "Successfully download the file: %s"%path
    except:
        print "Unable to download: % "%download_link
        
def unzip(zipFilePath, destDir):
    import os
    import zipfile
    zfile = zipfile.ZipFile(zipFilePath)
    print "Unzipping %s to %s"%(zipFilePath,destDir)
    for name in zfile.namelist():
        (dirName, fileName) = os.path.split(name)
        if fileName == '':
            # directory
            newDir = destDir + '/' + dirName
            if not os.path.exists(newDir):
                os.mkdir(newDir)
        else:
            # file
            fd = open(destDir + '/' + name, 'wb')
            fd.write(zfile.read(name))
            fd.close()
    zfile.close()

def is_admin():
    try:
        import ctypes, sys
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def Check_Pre_Req():
    
    admin_check = is_admin()
    if admin_check == False:
        raw_input("Please run this script as admin. Click on windows icon > type cmd OR search for cmd > right click on 'Command Line Prompt' and select 'Run as Administrator'.  Hit Enter button to exit")
        sys.exit()
    else:
        print "Admin check pass"
    
        
    if os.name != 'nt':
        print "System is not Windows"
        sys.exit(0)
    if sys.version_info[:2] != (2,7):
        print "Python version is not 2.7"
        sys.exit(0)
    if platform.architecture()[0] != '32bit':
        print "Python is not 32 bit. Some modules which are used require 32bit Python. Please uninstall 64bit Python, and install the 32bit Python, and try again."
        sys.exit(0)
    if 'setuptools' not in cmdline("easy_install --version"):
        print "'easy_install' is not installed"
        sys.exit(0)
    if 'pip' not in cmdline("pip --version"):
        print "pip is not installed, or not in your PATH variable."
        sys.exit(0)
    print "Prereq verified successfully"

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()


def main():
    sys.stdout = Logger()
    Check_Pre_Req()    
    Installer_With_Pip()
    Installer_With_Exe()
    Selenium_Driver_Files_Windows()
    print "Install Completed!"
    sys.stdout.close()

if __name__=="__main__":
    main()
