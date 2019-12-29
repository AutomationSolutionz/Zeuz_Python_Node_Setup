# Copyright 2016, Automation Solutionz
# ---

import subprocess
import os
import sys
import subprocess

install_str = "sudo pip install -U"



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

def Installer_With_Pip():
    # install pip
    try:
        install(cmd="sudo easy_install pip")
    except:
        print("Unable to install pip")
        
    
def basic_installation():
    #brew
    try:
        install(cmd='/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    except:
        print("Unable to install brew")
        
    #node
    try:
        install(cmd="brew install node")
    except:
        print("Unable to install node")
        
    #appium
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

## Install PIP
    print((78 * '-'))
    print ('Python PIP Installation')
    print((78 * '-'))

## Install PIP modules    
    # Installer_With_Pip()

    basic_installation()

    sys.stdout.close()

if __name__=="__main__":
    main()
