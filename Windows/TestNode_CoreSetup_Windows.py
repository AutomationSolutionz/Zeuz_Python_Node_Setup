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
    try:
        module_name = 'pip'
        install (type='pip', module_name = 'pip')
    except:
        print "unable to install/update %s"%module_name      

    # Check and install urllib3
    try:
        module_name="urllib3"
        install(type="pip", module_name="urllib3")
    except:
        print "unable to install/update %s"%module_name  
    

    
    
    # Check and install selenium
    try:
        module_name="selenium"
        install(type="pip", module_name="selenium")
    except:
        print "unable to install/update %s"%module_name  
    
    # Check and install wmi
    if os.name=='nt':
        try:
            module_name="wmi"
            install(type="pip", module_name="wmi")
        except:
            print "unable to install/update %s"%module_name  
    
    # Check and install requests
    try:
        module_name="requests"
        install(type="pip", module_name="requests")
    except:
        print "unable to install/update %s"%module_name  
        
    # Check and install six
    try:
        module_name="six"
        install(type="pip", module_name="six")
    except:
        print "unable to install/update %s"%module_name  
    
    # Check and install pillow
    try:
        module_name="Pillow"
        install(type="pip", module_name="Pillow")
    except:
        print "unable to install/update %s"%module_name  
    
    # Check and install poster
    try:
        module_name="poster"
        install(type="pip", module_name="poster")
    except:
        print "unable to install/update %s"%module_name  

    # Check and install wheel
    try:
        module_name="wheel"
        install(type="pip", module_name="wheel")
    except:
        print "unable to install/update %s"%module_name

    # Check and install python-dateutil
    try:
        module_name="python-dateutil"
        install(type="pip", module_name="python-dateutil")
    except:
        print "unable to install/update %s"%module_name

    # Check and install dropbox
    try:
        module_name="dropbox"
        install(type="pip", module_name="dropbox")
    except:
        print "unable to install/update %s"%module_name
    
    #install .NET support for python
    try:
        module_name="pythonnet"
        install(type="pip", module_name="pythonnet")
    except:
        print "unable to install/update %s"%module_name

    #install pyautoit support for python
    try:
        module_name="pyautoit"
        install(type="pip", module_name="pyautoit")
    except:
        print "unable to install/update %s"%module_name

    #install pywinauto support for python
    try:
        module_name="pywinauto"
        install(type="pip", module_name="pywinauto")
    except:
        print "unable to install/update %s"%module_name		
    # Check and install lxml
'''
    try:
        module_name="lxml"
        install(type="pip", module_name="lxml")
    except:
        print "unable to install/update %s"%module_name
'''
def Easy_Installer():

    try:
        print "skipping psycopg2 install as its not needed"
        #psycopg2_easy_install = "easy_install http://www.stickpeople.com/projects/python/win-psycopg/2.6.0/psycopg2-2.6.0.win32-py2.7-pg9.4.1-release.exe"
        #install(cmd=psycopg2_easy_install)
        # print "skipping wx install .."
        install(type="pip", module_name="wx")
        #wx_install = "pip install --upgrade --trusted-host wxpython.org --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix"
        #install(cmd=wx_install)
    except:
        print "unable to install/update wxpython"
    
    try:
        import funkload
    except ImportError as e:
        try:
            funkload_easy_install = "easy_install https://github.com/nuxeo/FunkLoad/archive/master.zip"
            install(cmd=funkload_easy_install)
        except:
            print "unable to install/update ImageGrab"

    # Check and install simplejson
    try:
        import simplejson
    except ImportError as e:
        try: 
            simplejson_easy_install = "easy_install https://github.com/simplejson/simplejson/archive/master.zip"
            install(cmd=simplejson_easy_install)
        except:
            print "unable to install/update win32api"

    # Check and install psutil
    try:
        import psutil
    except ImportError as e:
        try: 
            psutil_easy_install = "easy_install psutil"
            install(cmd=psutil_easy_install)
        except:
            print "unable to install/update psutil"

def Installer_With_Exe():
    
    # Check and install psycopg2
    '''try:
        print "removing psycopg2"
        #psycopg2_easy_install = "easy_install http://www.stickpeople.com/projects/python/win-psycopg/2.6.0/psycopg2-2.6.0.win32-py2.7-pg9.4.1-release.exe"
       # install(cmd=psycopg2_easy_install)
    except:
        print "unable to install/update psycopg2"'''
    

    # Check and install win32api
    try:
        import win32api
    except ImportError as e:
        try: 
            win32api_easy_install = "easy_install http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download"
            install(cmd=win32api_easy_install)
        except:
            print "unable to install/update win32api"
        
    #pill
    #http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
    try:
        from PIL import ImageGrab
    except ImportError as e:
        try:
            PIL_easy_install = "easy_install http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe"
            install(cmd=PIL_easy_install)
        except:
            print "unable to install/update ImageGrab"
   
 
    
#     try:
#         import lxml
#     except ImportError as e:
    try: 
        print "installing lxml"
        
        lxml_easy_install = "easy_install https://pypi.python.org/packages/2.7/l/lxml/lxml-3.4.1.win32-py2.7.exe"
        install(cmd=lxml_easy_install)
    except:
        print "unable to install/update lxml"

#   install PyQt4
    try:
        import PyQt4
    except ImportError as e:
        try:
            PIL_easy_install = 'easy_install https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe'
            install(cmd=PIL_easy_install)
        except:
            print "unable to install/update PyQt4"
        
    


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

def Check_Pre_Req():
    if os.name != 'nt':
        print "System is not Windows"
        sys.exit(0)
    if sys.version_info[:2] != (2,7):
        print "Python version is not 2.7"
        sys.exit(0)
    if platform.architecture()[0] != '32bit':
        print "Python is not 32 bit"
        sys.exit(0)
    if 'setuptools' not in cmdline("easy_install --version"):
        print "easy_install is not installed"
        sys.exit(0)
    if 'pip' not in cmdline("pip --version"):
        print "pip is not installed"
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
    Easy_Installer()

    sys.stdout.close()

if __name__=="__main__":
    main()
