# Copyright 2015, Automation Solutionz
# ---

import subprocess
import shutil
import os, os.path
import sys

from _winreg import (
    CloseKey, OpenKey, QueryValueEx, SetValueEx,
    HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE,
    KEY_ALL_ACCESS, KEY_READ, REG_EXPAND_SZ, REG_SZ
)

install_str = "python -m pip install -U"

############################# Windows registry editing #######################################
def env_keys(user=True):
    ''' Get root and subkey for the machine or user environment '''
    if user:
        root = HKEY_CURRENT_USER
        subkey = 'Environment'
    else:
        root = HKEY_LOCAL_MACHINE
        subkey = r'SYSTEM\ControlSet001\Control\Session Manager\Environment'
    return root, subkey


def get_env(name, user=True):
    ''' Read the variable and return '''
    root, subkey = env_keys(user)
    key = OpenKey(root, subkey, 0, KEY_READ)
    try:
        value, _ = QueryValueEx(key, name)
    except WindowsError:
        return ''
    return value


def set_env(name, user, value):
    ''' Write variable data to the registry key '''
    root, subkey = env_keys(user)
    key = OpenKey(root, subkey, 0, KEY_ALL_ACCESS)
    SetValueEx(key, name, 0, REG_EXPAND_SZ, value)
    CloseKey(key)
    #SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, subkey) # Causes a hang, not sure if actually needed

def append_env(name, user, value):
    ''' Append the new data to the variable, assuming it's not already there '''
    cur_value = get_env(name, user=user)
    for path in cur_value.split(';'): # Do not add if already in variable
        if path.upper() == value.upper():
            return
    value = cur_value + ';' + value
    set_env(name, user, value)
############################# Windows registry editing #######################################

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
        module_name = "Appium-Python-Client"
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
    print "installing node and npm"
    os.system(os.getcwd().replace('\\','/')+'/backupDriverFiles/Android/appium.bat')
    install(cmd="npm install -g node_gyp")
    print "installing appium 1.6.3"
    install(cmd="npm install -g appium@1.6.3")
    print "appium 1.6.3 installed successfully"


def Install_Android_SDK():
    import webbrowser
    webbrowser.open_new('http://filehippo.com/download_android_sdk/')
    raw_input('Press Any Key when Android SDK installed')

    if os.path.isdir(os.path.join('C:', os.sep, 'Program Files', 'Android', 'android-sdk')) or os.path.isdir(os.path.join(os.environ["LocalAppData"], 'Android', 'android-sdk')):
        os.environ['ANDROID_HOME'] = os.environ["LocalAppData"]+'\\Android\\android-sdk'
        os.environ['ADT_HOME'] = os.environ["LocalAppData"]+'\\Android\\android-sdk'
        os.environ['PATH']+='%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools' # Set locally in command prompt?
        append_env('PATH', False, os.environ['ANDROID_HOME']) # Store in PATH variable in registry for entire machine, so adb is in the path
        
        subprocess.Popen([os.path.join(os.environ['ANDROID_HOME'], 'SDK Manager.exe')]) # Execute SDK Manager, so the user can install missing packages
        raw_input('Please install all suggested packages, and press any key when complete')
        
        print "----------------------------------"
        print "Android SDK installed successfully"
        print "----------------------------------"
    else:
        print "-------------------------"
        print "Android SDK not installed"
        print "-------------------------"
        quit()

def Install_Java_JDK():
    import webbrowser
    import glob
    webbrowser.open_new('http://www.oracle.com/technetwork/java/javase/downloads/index.html')
    raw_input('Press Any Key when Java JDK installed')

    installed = False
    for name in glob.glob(os.path.join('C:', os.sep, 'Program Files', 'Java', 'jdk*')): # os.environ["ProgramFiles"] < This Gets Program Files(x86) for some reason, so we can't use it
        os.environ['JAVA_HOME'] = name
        os.environ['PATH']+='%JAVA_HOME%;%JAVA_HOME%\bin'
        print "----------------------------------"
        print "JAVA JDK installed successfully"
        print "----------------------------------"
        installed = True

    if not installed:
        print "-------------------------"
        print "JAVA JDK not installed"
        print "-------------------------"
        quit()

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
