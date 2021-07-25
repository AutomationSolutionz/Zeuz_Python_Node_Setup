# Copyright 2016, Automation Solutionz
# ---

import subprocess
import os
import sys
import subprocess

install_str = "pip3 install -U"

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""
    
    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)

    else:
        command = cmd
    print("Installing: %s " %command)
    status, output = subprocess.getstatusoutput(command)
    print(output)
    print((78 * '-'))


def basic_installation():
    #node
    try:
        install(cmd="brew install node")
    except:
        print("Unable to install node")

    # Install java
    try:
        install(cmd="brew cask install adoptopenjdk")
    except:
        print("Unable to install adoptopenjdk (Java)")
    
    # Set JAVA_HOME variable
    try:
        print("Setting JAVA_HOME for Bash (~/.bashrc)")
        output = os.system('echo "export JAVA_HOME=`/usr/libexec/java_home`" >> ~/.bashrc')
        print(output)

        print("Setting JAVA_HOME for ZSH (~/.zshrc)")
        output = os.system('echo "export JAVA_HOME=`/usr/libexec/java_home`" >> ~/.zshrc')
        print(output)
    except:
        print("Unable to set JAVA_HOME variable. You may not be able to run Android automation if this is not set properly")

    # ADB for android
    try:
        install(cmd="brew cask install android-platform-tools")
    except:
        print("Unable to install adb. Zeuz Node will be unable to detect devices if adb is not working.")
    
    try:
        install(cmd="npm install -g appium@1.4.16")
    except:
        print("Unable to install appium")


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_Android_Mac_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()


def main():
    sys.stdout = Logger()

    basic_installation()

    sys.stdout.close()

if __name__=="__main__":
    main()

