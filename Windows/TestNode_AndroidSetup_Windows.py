# Copyright 2015, Automation Solutionz
# ---

import subprocess
import shutil
import os
import sys

install_str = "python -m pip install -U"

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
    subprocess.call(command, shell=True)

def Installer_With_Pip():
    try:
        speech_easy_install = "pip install SpeechRecognition"
        install(cmd=speech_easy_install)
    except:
        print "unable to install/update SpeechRecognition"
        
    try:
        install(type="pip", module_name="Appium-Python-Client")
    except:
        print "unable to install/update %s"%module_name

def Easy_Installer():

    try:
        import uiautomator
    except ImportError as e:
        try:
            ui_easy_install="easy_install https://github.com/xiaocong/uiautomator/archive/master.zip"
            install(cmd=ui_easy_install)
        except:
            print "unable to install/update uiautomator"
	
def Installer_With_Exe():
    try:
        import pyaudio
    except ImportError as e:
        try:
            pyaudio_easy_install = "easy_install http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.8.py27.exe"
            install(cmd=pyaudio_easy_install)
        except:
            print "unable to install/update pyaudio"
        
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

def Install_Appium():
    #first give the ant setup
    ant_path=os.getcwd()+os.sep+'backupDriverFiles'+os.sep+'Android'+os.sep+'apache-ant-1.9.5-bin.zip'
    unzip(ant_path,'C:\Python27\Lib\site-packages')
    os.environ['ANT_HOME']='C:\Python27\Lib\site-packages\apache-ant-1.9.5\bin'
    os.environ['PATH']+='C:\Python27\Lib\site-packages\apache-ant-1.9.5\bin'
    maven_path=os.getcwd()+os.sep+'backupDriverFiles'+os.sep+'Android'+os.sep+'apache-maven-3.3.3-bin.zip'
    unzip(maven_path,'C:\Python27\Lib\site-packages')
    os.environ['PATH']+='C:\Python27\Lib\site-packages\apache-maven-3.3.3\bin;'
    os.system(os.getcwd().replace('\\','/')+'/backupDriverFiles/Android/appium.bat')

def Install_Android_SDK():
    import webbrowser
    webbrowser.open_new('http://developer.android.com/sdk/index.html')
    raw_input('Press Any Key when Android SDK installed')

    if os.path.isdir(os.environ["LocalAppData"]+'\\Android\\sdk'):        
        os.environ['ANDROID_HOME'] = os.environ["LocalAppData"]+'\\Android\\sdk'
        os.environ['ADT_HOME'] = os.environ["LocalAppData"]+'\\Android\\sdk'
        os.environ['PATH']+='%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools'
        print "----------------------------------"
        print "Android SDK installed successfully"
        print "----------------------------------"

    else:
        print "-------------------------"
        print "Android SDK not installed"
        print "-------------------------"


def Install_Java_JDK():
    import webbrowser
    import glob
    webbrowser.open_new('http://www.oracle.com/technetwork/java/javase/downloads/index.html')
    raw_input('Press Any Key when Java JDK installed')
    
    for name in glob.glob(os.environ["ProgramFiles"]+'\\Java\\jdk*'):
        os.environ['JAVA_HOME'] = name
        os.environ['PATH']+='%JAVA_HOME%;%JAVA_HOME%\bin'
        print "----------------------------------"
        print "JAVA JDK installed successfully"
        print "----------------------------------"

    else:
        print "-------------------------"
        print "JAVA JDK not installed"
        print "-------------------------"


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_Android_Windows_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()


def main():
    sys.stdout = Logger()

    Installer_With_Pip()
    Installer_With_Exe()
    Easy_Installer()
    Install_Java_JDK()
    Install_Android_SDK()
    Install_Appium()

    sys.stdout.close()

if __name__=="__main__":
    main()
