# Copyright 2016, Automation Solutionz Inc.
# ---


import subprocess
import os
import sys
import commands
import getpass # For check_if_ran_with_sudo()

install_str = "sudo pip install -U pip"
apt_get_str = "sudo apt-get install"
br_install_str = "brew install"

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""

    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
        print "Installing: %s " %command
    elif type == "apt-get":
        command = "%s %s --yes" % (apt_get_str, module_name)
        print "Installing: %s " %command
    else:
        command = cmd
        print "Running: %s " %command

    status, output = commands.getstatusoutput(command)
    print output
    print "\n"
    print (78 * '-')
    print "\n"
    print "\n"


def Installer_With_Brew():
    try:
        install(cmd="brew doctor")
    except:
        print "unable to run brew doctor"
    
    try:
        install(cmd="brew update")
    except:
        print "unable to update brew"
        
    try:
        install(cmd="brew install perl")
    except:
        print "unable to install perl"
    
    """try:
        install(cmd="sudo chown -R $USER /usr/local")
    except:
        print "Unable to run the command" """
    
    # install node
    try:
        install(cmd="brew install node")
    except:
        print "unable to install node"
        
    try:
        install(cmd="brew upgrade node")
    except:
        print "unable to update node"


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_Android_Linux_Part_2_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def close(self):
        self.log.close()

def Installing_sdk():
    try:
        install(cmd="source ~/.bashrc")
    except:
        print "Unable to set paths"
        
    print "Opening android SDK to install necessary platform and packages..."
    try:
        install(cmd="android update sdk")
    except:
        print "Unable to update sdk"

    
    print "Please make sure latest platform and tools are installed via GUI."
    try:
        install(cmd="android")
    except:
        print "Unable to open sdk"


def Installing_appium():
    try:
        install(cmd="npm install")
    except:
        print "Unable to install necessary packages"

    # Get version from user, or use latest
    ver = raw_input("Specify appium version or leave blank for latest:")
    if ver == '':
        print "Installing latest"
    else:
        ver = '@' + ver.strip()
        print "Installing", ver
            
    try:
        install(cmd="npm install -g appium" + ver)
    except:
        print "Unable to install appium"

    try:
        install(cmd="npm install wd")
    except:
        print "Unable to install appium client"
        
        
def Manual_part():
    print "\n"
    print (78 * '-')
    print "\n"
    
    try:
        status, output = commands.getstatusoutput("brew -v")
        print output
        if "not found" in output:
            print "Please open up a new terminal and run the command \"ruby -e \"$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install)\"\" (Excluding the first/outer quotation)"
        else:
            print "Brew is installed successfully!"
    except:
        print "Unable to run the command"
        
    
    print "\n"
    print (78 * '-')
    print "\n"
        
    try:
        status, output = commands.getstatusoutput("npm -v")
        print output
        if "not installed" in output:
            print "Please open up a new terminal and run the command \"brew install node\" (Excluding the quotation)"
        else:
            print "Node/NPM is installed successfully!"
            
    except:
        print "Unable to run the command"
        
        
    
    print "\n"
    print (78 * '-')
    print "\n"
    
    """try:
        status, output = commands.getstatusoutput("appium")
        print output
        if "command not found" in output:
            print "Please open up a new terminal and run the command \"npm install -g appium@1.4.16\" (Excluding the quotation)"
        else:
            print "Appium is installed successfully!"
    except:
        print "Unable to run the command" """
    
    try:
        status, output = commands.getstatusoutput("appium -v")
        print output
        if "not found" in output:
            print "Please open up a new terminal and run the command \"npm install -g appium@1.4.16\" (Excluding the quotation)"
        else:
            print "Appium is installed successfully!"
    except:
        print "Unable to run the command"
        
    
    print "\n"
    print (78 * '-')
    print "\n"
    

def check_if_ran_with_sudo():
    global sudo_pass
    sudo_pass = None
    if os.getuid() == 0:
        return True
    else:
        max_try = 3
        counter=0
        have_pass = False
        while counter != max_try:
            print "This program needs sudo access.  please provide sudo password"
            passwd = getpass.getpass()
            print "checking to see if you have entered correct sudo"
            command = "echo 'sudo check'"
            p = os.system('echo %s|sudo -S %s' % (passwd, command)) # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
            if p == 256:
                print "You didnt enter the correct sudo password.  Chances left: %s"%(max_try-counter-1)
                counter = counter+1
            else:
                print "sudo authentication verified!"
                have_pass = True
                break    
        if have_pass == False:
            return False
        else:   
            print "You'll have to enter it later when prompted"
            sudo_pass = passwd
            return False
        
def main():
    # Make sure we didn't start with sudo, but we can setup the environment
    if check_if_ran_with_sudo():
        print "Error: This script was started with sudo. You must run it without sudo privileges, and enter the password only when prompted."
        quit()
    else:
        print "Not run with sudo, good to continue"

    # Start logger
    sys.stdout = Logger()

    ## Install brew modules
    Installer_With_Brew()

    ## android install
    Installing_sdk()

    ## appium install
    Installing_appium()
    
    ## manual install
    Manual_part()

    sys.stdout.close()

if __name__=="__main__":
    main()
