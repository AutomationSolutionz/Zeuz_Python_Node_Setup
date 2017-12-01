# Copyright 2016, Automation Solutionz
# ---

import subprocess
import os
import sys
import commands

install_str = "sudo pip install -U pip"
apt_get_str = "sudo apt-get install"


# Installation function
def install(type="", module_name="", module_version=None, cmd=""):
    command = ""

    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    elif type == "apt-get":
        command = "%s %s --yes" % (apt_get_str, module_name)
    else:
        command = cmd
    print "Installing: %s " % command
    status, output = commands.getstatusoutput(command)
    print output
    print (78 * '-')


def Installer_With_Pip():
    # install pip
    try:
        install(cmd="sudo easy_install pip")
    except:
        print "Unable to install pip"


def basic_installation():
    # brew
    try:
        install(
            cmd='/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    except:
        print "Unable to install brew"

    # node
    try:
        install(cmd="brew install node")
    except:
        print "Unable to install node"

    # ideviceinstaller
    try:
        install(cmd="brew install ideviceinstaller")
    except:
        print "Unable to install ideviceinstaller"

    # carthage
    try:
        install(cmd="brew install carthage")
    except:
        print "Unable to install carthage"

    # appium
    try:
        install(cmd="npm install -g appium")
    except:
        print "Unable to install appium"

    # carthage
    try:
        install(cmd="brew unlink libimobiledevice")
        install(cmd="brew install libimobiledevice --HEAD")
    except:
        print "Unable to install libimobiledevice"


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_iOS_Mac_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()


def main():
    sys.stdout = Logger()

    ## Install PIP
    print (78 * '-')
    print ('Python PIP Installation')
    print (78 * '-')
    os.system("sudo add-apt-repository universe")
    os.system("sudo apt-get update --yes")
    install(type="apt-get", module_name="python-pip")

    ## Install PIP modules
    Installer_With_Pip()

    basic_installation()

    sys.stdout.close()


if __name__ == "__main__":
    main()