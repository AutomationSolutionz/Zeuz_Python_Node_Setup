# Copyright 2016, Automation Solutionz Inc.
# ---


import subprocess
import os
import sys
import commands
import getpass # For check_if_ran_with_sudo()

install_str = "sudo pip install -U pip"
apt_get_str = "sudo apt-get install"
br_install_str = "brew install -v"

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""

    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
        print "Installing: %s " %command
    elif type == "brew":
        command = "%s %s" % (br_install_str, module_name)
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

def basic_installation():
    print (78 * '-')
    print "Sit tight! This setup may require password couple of times and commands may seem stuck while running in background. Please be patient."
    print (78 * '-')
    
    try:
        install(cmd="sudo dpkg --configure -a")
    except:
        print "Unable to configure dpkg"
        
    #pip install
    try:
        install(type = "apt-get", module_name = "python-pip")
    except:
        print "Unable to install pip"

    #uiautomator
    try:
        install(type = "pip", module_name = "uiautomator")
    except:
        print "Unable to install uiautomator"
        
    """try:
        install(cmd="sudo chown -R $USER /usr/local")
    except:
        print "Unable to run the command"
        
    try:
        install(cmd = "curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -")
    except:
        print "Unable to proceed with node installation"
        
    #npm install
    try:
        install(type = "apt-get", module_name = "npm")
    except:
        print "Unable to install npm"
        
        
    #nodejs install
    try:
        install(type = "apt-get", module_name = "nodejs")
    except:
        print "Unable to install nodejs" """

def Installer_With_Brew():

    #brew install
    print "Installing brew installer..."
    try:
        install(type="apt-get" ,module_name = "build-essential curl git m4 python-setuptools ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev")
    except:
        print "Unable to install brew requirements"

    try:
        install(cmd="sudo dpkg --configure -a")
    except:
        print "Unable to configure dpkg"
        
    try:
        install(type="apt-get",  module_name = "build-essential curl git python-setuptools ruby")
    except:
        print "Unable to install dependencies"
        
    try:
        install(cmd='ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install)"')
    except:
        print "Unable to install Linuxbrew"

    try:
        print "Don't panic! This step might take a while."
        install(cmd="sudo apt-get update -y")
    except:
        print "Unable to update"
    '''
    # we shouldnt do upgrade on 
    try:
        print "Grab a coffee! This step might take longer. If you don't have time to wait then press 'CTRL + C' just once."
        install(cmd="sudo apt-get upgrade -y")
    except:
        print "Unable to upgrade"
    '''
        
    try:
        install(type="apt-get" ,module_name="build-essential make cmake scons curl git ruby autoconf automake autoconf-archive gettext libtool flex bison  libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev")
    except:
        print "Unable to install brew requirements"

    try:
        install(cmd="sudo rm -rf ~/.linuxbrew")
    except:
        print "Unable to update"

    try:
        install(cmd="git clone https://github.com/Homebrew/linuxbrew.git ~/.linuxbrew")
    except:
        print "Unable to install brew"

    try:
        install(cmd="echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:/usr/local/lib64/pkgconfig:/usr/lib64/pkgconfig:/usr/lib/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib64/pkgconfig:/usr/share/pkgconfig:$PKG_CONFIG_PATH' >>~/.bashrc")
        install(cmd="echo 'export LINUXBREWHOME=$HOME/.linuxbrew' >>~/.bashrc")
        install(cmd="echo 'export PATH=$LINUXBREWHOME/bin:$PATH' >>~/.bashrc")
        install(cmd="echo 'export MANPATH=$LINUXBREWHOME/man:$MANPATH' >>~/.bashrc")
        install(cmd="echo 'export INFOPATH=$LINUXBREWHOME/info:$INFOPATH' >>~/.bashrc")
        install(cmd="echo 'export PKG_CONFIG_PATH=$LINUXBREWHOME/lib64/pkgconfig:$LINUXBREWHOME/lib/pkgconfig:$PKG_CONFIG_PATH' >>~/.bashrc")
        install(cmd="echo 'export LD_LIBRARY_PATH=$LINUXBREWHOME/lib64:$LINUXBREWHOME/lib:$LD_LIBRARY_PATH' >>~/.bashrc")
        #install(cmd="source ~/.bashrc")
        print (78 * '-')
    except:
        print "Unable to install brew"

    '''try:
        install(type="apt-get", module_name="linuxbrew-wrapper")
    except:
        print "Unable to install linuxbrew"'''


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_Android_Linux_Part_1_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def close(self):
        self.log.close()

def get_latest_android_sdk_url():
    #xml = 'https://dl.google.com/android/repository/repository-11.xml'
    xml = 'https://dl.google.com/android/repository/repository-12.xml' # Not sure why the number changes, or how to predict
    url = 'https://dl.google.com/android/repository/'

    # Get xml file containing filenames
    status, data = commands.getstatusoutput("curl -s %s" % xml)
    if status != 0:
        return False
    
    # Find latest android build tool archive (quick and dirty version)
    archives = []
    marker = 0
    data = data.split("\n") # Split string into list to make it easy to work with
    for line in data: # For each line
        if '<sdk:build-tool>' in line: # Identify buil marker
            marker = 1
        elif '</sdk:build-tool>' in line: # End of marker
            marker = 0
        elif '<sdk:url>' in line and 'linux' in line and marker == 1: # Valid linux archive
            line = line.replace('<sdk:url>', '')
            line = line.replace('</sdk:url>', '')
            line = line.strip()
            #archives.append(line) # Can store all versions if we want multiple choices
            return "%s%s" % (url, line) # Stop here - first result is the newest version
    return False # Should not get here - means we did not find the droids we were looking for

def Installing_sdk():
    print (78 * '-')
    print "Installing JDK and android SDK..."

    ## Install android sdk

    try:
        install(type="apt-get", module_name="default-jdk")
    except:
        print "Unable to install jdk"

    print "Downloading android SDK..."
    
    #sdk_url = get_latest_android_sdk_url() # !!! Newest version of android sdk is untested, so this is disabled for now
    #if sdk_url:
    #    print sdk_url
    #else:
    #    print "Error: Could not find latest Android SDK. Using default version."
    try:
        install(cmd="wget http://dl.google.com/android/android-sdk_r24.4.1-linux.tgz")
    except:
        print "Unable to download android sdk"

    try:
        install(cmd="sudo apt-get update -y")
    except:
        print "Unable to extract sdk"

    try:
        install(cmd="tar -xvf android-sdk_r24.4.1-linux.tgz -C $HOME")
    except:
        print "Unable to extract sdk"

    try:
        install(type="apt-get", module_name="android-tools-adb")
    except:
        print "Unable to install adb"

    try:
        install(cmd="echo 'export ANDROID_HOME=$HOME/android-sdk-linux' >>~/.bashrc")
        install(cmd="echo 'export PATH=${PATH}:$HOME/android-sdk-linux/platform-tools:$HOME/android-sdk-linux/tools:$HOME/android-sdk-linux/build-tools/24.4.1/' >>~/.bashrc")
        #install(cmd="source ~/.bashrc")
    except:
        print "Unable to set android paths"
         
    try:
        install(cmd="sudo apt-get install libc6:i386 libstdc++6:i386 --force-yes -y")
    except:
        print "Unable to install libc6"

    try:
        install(cmd="sudo apt-get install zlib1g:i386 --force-yes -y")
    except:
        print "Unable to install aapt"


def Uninstalling_appium():
    try:
        import appium
        install(cmd="npm uninstall -g appium")
    except:
        print "Appium not found"

    try:
        install(type="pip", module_name="Appium-Python-Client")
    except:
        print "Unable to install appium"

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

    ## Install basic modules
    basic_installation()

    ## Install brew modules
    Installer_With_Brew()

    ## android install
    Installing_sdk()

    ## appium install
    Uninstalling_appium()

    sys.stdout.close()

if __name__=="__main__":
    main()
